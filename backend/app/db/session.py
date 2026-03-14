from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase URL needs to be converted for asyncpg
DB_URL = os.getenv("DB_URL", "").strip().strip("'").strip('"')
if DB_URL.startswith("postgresql://"):
    ASYNC_DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    ASYNC_DB_URL = DB_URL


engine = create_async_engine(
    ASYNC_DB_URL, 
    echo=True,
    connect_args={"statement_cache_size": 0}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
