from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import AsyncGenerator

import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_name = os.getenv("POSTGRES_DB")

postgres_file_name = "postgres.db"

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def create_db_and_tables():
    print("Startup: Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Startup: Database tables check/creation complete.")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session: # Manages context
        try:
            yield session # Provides session to endpoint
            await session.commit() # Commits if endpoint successful
        except Exception:
            await session.rollback() # Rolls back on error
            raise

db_dependency = Annotated[AsyncSession, Depends(get_db)]
