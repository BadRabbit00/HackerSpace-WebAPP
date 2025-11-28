"""
Health check router for monitoring application status.
"""
from typing import Any, Dict

import redis.asyncio as redis
from aio_pika import Connection
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_rabbitmq, get_redis

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "healthy"}


@router.get("/health/detailed")
async def detailed_health_check(
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
    rabbitmq: Connection = Depends(get_rabbitmq),
) -> Dict[str, Any]:
    """Detailed health check with all service statuses."""
    health_status: Dict[str, Any] = {
        "status": "healthy",
        "services": {},
    }

    # Check PostgreSQL
    try:
        await db.execute(text("SELECT 1"))
        health_status["services"]["database"] = {"status": "healthy"}
    except Exception as e:
        health_status["services"]["database"] = {"status": "unhealthy", "error": str(e)}
        health_status["status"] = "unhealthy"

    # Check Redis
    try:
        await redis_client.ping()
        health_status["services"]["redis"] = {"status": "healthy"}
    except Exception as e:
        health_status["services"]["redis"] = {"status": "unhealthy", "error": str(e)}
        health_status["status"] = "unhealthy"

    # Check RabbitMQ
    try:
        if rabbitmq and not rabbitmq.is_closed:
            health_status["services"]["rabbitmq"] = {"status": "healthy"}
        else:
            health_status["services"]["rabbitmq"] = {"status": "unavailable"}
    except Exception as e:
        health_status["services"]["rabbitmq"] = {"status": "unhealthy", "error": str(e)}
        health_status["status"] = "unhealthy"

    return health_status
