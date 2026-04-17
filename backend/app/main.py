from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.db.session import engine, Base
from app.models.chat import Chat, Message
from app.models.user import User
from app.models.organization import Organization

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "backend running"}
