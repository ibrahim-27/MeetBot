from dotenv import load_dotenv

load_dotenv()

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def read_root():
    return {"status": "backend running"}
