from dotenv import load_dotenv

load_dotenv()

import os
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.db.session import Base, engine
from app.jobs.transcript_job import run_transcript_summary_job
from app.models.chat import Chat, Message
from app.models.meeting import Meeting
from app.models.meeting_chunk import MeetingChunk

from app.models.organization import Organization
from app.models.user import User

app = FastAPI()
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if not scheduler.running:
        scheduler.add_job(
            run_transcript_summary_job,
            trigger=CronTrigger(hour=0, minute=0),
            id="transcript_summary_job",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    if scheduler.running:
        scheduler.shutdown(wait=False)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

# Serve frontend static files
frontend_out = Path(__file__).parent.parent.parent / "frontend" / "out"
if frontend_out.exists():
    # Mount Next.js assets
    next_dir = frontend_out / "_next"
    if next_dir.exists():
        app.mount("/_next", StaticFiles(directory=next_dir), name="next")


@app.get("/")
def read_root():
    # Serve index.html if frontend is built
    index_path = frontend_out / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    return {"status": "backend running"}


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Skip API routes and Next.js assets
    if full_path.startswith("api/") or full_path.startswith("_next/"):
        return {"error": "Not found"}
    
    file_path = frontend_out / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    # Fallback to index.html for SPA routing
    index_path = frontend_out / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    
    return {"error": "Not found"}
