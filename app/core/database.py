# -*- coding: UTF-8 -*-
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from .config import DB_URL, setup_logs


logger = setup_logs()


async_engine = create_async_engine(
    DB_URL,
    echo=False,
    future=True
)


AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def wait_for_db(max_retries: int = 30, retry_interval: int = 2):
    for attempt in range(1, max_retries + 1):
        try:
            async with async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Database connection established successfully")
            return True
        except OperationalError as e:
            logger.warning(f"Database connection attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                await asyncio.sleep(retry_interval)
            else:
                logger.error("Failed to connect to database after all retries")
                raise
        except Exception as e:
            logger.error(f"Unexpected error while connecting to database: {e}")
            raise
