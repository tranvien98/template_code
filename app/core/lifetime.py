import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logging_config import setup_logging
# from app.migrations.runner import run_migrations

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the db
    setup_logging()
    # await run_migrations()
    logging.info("Startup complete")

    yield
    logging.info("Shutdown complete")
