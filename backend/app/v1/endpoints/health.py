import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.user_service import check_database_connection

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health", response_model=dict[str, Any])
async def health_check(session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    try:
        database_is_healthy = await check_database_connection(session)
    except SQLAlchemyError as exc:
        logger.exception("Database health check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable",
        ) from exc

    if not database_is_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database health check returned an unexpected result",
        )

    return {
        "success": True,
        "data": {"status": "ok", "database": "connected"},
        "error": None,
    }
