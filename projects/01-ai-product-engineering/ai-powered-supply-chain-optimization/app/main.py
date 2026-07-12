from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.inventory import router as inventory_router
from app.core.config import settings
from app.db.database import initialize_database


APP_NAME = settings.app_name
APP_VERSION = settings.app_version


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    initialize_database()
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Backend API for an AI-powered supply-chain optimization platform "
        "supporting forecasting, inventory optimization, procurement, "
        "logistics, and operational decision support."
    ),
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


app.include_router(
    inventory_router,
    prefix=settings.api_prefix,
)


@app.get(
    "/",
    tags=["System"],
    summary="API information",
)
async def root() -> dict[str, str]:
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "operational",
        "environment": settings.environment,
        "documentation": "/docs",
        "health_check": "/health",
        "inventory_api": f"{settings.api_prefix}/inventory",
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
)
async def health_check() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": APP_NAME,
            "version": APP_VERSION,
            "environment": settings.environment,
        },
    )