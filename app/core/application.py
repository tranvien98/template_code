import os
import logging
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.lifetime import lifespan
from app.core.routers_api import router as router_api_v1
from config import settings


APP_ROOT = Path(__file__).parent.parent

DESCRIPTION = """
This API for Sun platform.
"""


def get_app() -> FastAPI:
    """
    Create FastAPI application.

    :return: FastAPI application.
    """

    app = FastAPI(
        title="SUN API",
        description=DESCRIPTION,
        version="0.1.1",
        lifespan=lifespan,
        openapi_url="/api/openapi.json"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(router_api_v1, prefix="/api")

    os.makedirs(os.path.join(settings.STORAGE, 'files'), exist_ok=True)
    app.mount("/resources/files", StaticFiles(directory=os.path.join(settings.STORAGE, 'files')), name="file")
    @app.exception_handler(RequestValidationError)



    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logging.error(f"RequestValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.errors()},
        )
    return app
