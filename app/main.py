# -*- coding: UTF-8 -*-
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import async_engine, wait_for_db
from app.models.incident_models import Base
from app.api.incident_endpoints import router as incident_router
from app.core.config import setup_logs
from app.core.middleware import log_requests_middleware


logger = setup_logs()


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Incident Management API")

    logger.info("Waiting for database...")
    await wait_for_db()

    logger.info("Creating database tables...")
    await create_tables()
    
    logger.info("Incident Management API started successfully")
    
    yield

    logger.info("Shutting down Incident Management API")


app = FastAPI(
    title="Incident Management API",
    version="v0.0.1",
    lifespan=lifespan
)


app.middleware('http')(log_requests_middleware)
app.include_router(incident_router)


@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}
