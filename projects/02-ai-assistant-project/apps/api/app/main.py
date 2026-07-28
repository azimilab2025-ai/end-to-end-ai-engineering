from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0", debug=settings.app_debug)
app.include_router(api_router, prefix=settings.api_v1_prefix)

@app.get("/", tags=["Platform"])
async def root() -> dict[str, str]:
    return {"name": settings.app_name, "status": "running"}
