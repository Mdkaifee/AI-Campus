"""Health endpoints."""

from fastapi import APIRouter

from app.database.mongodb import check_mongo_health
from app.schemas.response import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="API health check",
    description="Returns ok when the API process is running. "
    "Also reports MongoDB connectivity.",
)
async def health() -> HealthResponse:
    db_ok = await check_mongo_health()
    return HealthResponse(
        status="ok" if db_ok else "degraded",
        database="ok" if db_ok else "unavailable",
    )
