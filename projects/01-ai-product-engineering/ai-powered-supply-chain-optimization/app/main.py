from fastapi import FastAPI
from fastapi.responses import JSONResponse

APP_NAME = "AI-Powered Supply Chain Optimization API"
APP_VERSION = "0.1.0"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Backend API for an AI-powered supply-chain optimization platform "
        "supporting forecasting, inventory optimization, procurement, "
        "logistics, and operational decision support."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
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
        "documentation": "/docs",
        "health_check": "/health",
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
        },
    )