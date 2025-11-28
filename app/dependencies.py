"""
Application dependencies for dependency injection.
"""
from typing import AsyncGenerator, Optional

import redis.asyncio as redis
from aio_pika import Connection, connect_robust

from app.config import Settings, get_settings
from app.database import get_db  # Re-export for convenience

# Global connection instances
_redis_client: Optional[redis.Redis] = None
_rabbitmq_connection: Optional[Connection] = None


# Re-export get_db from database module
__all__ = ["get_db", "get_config", "get_redis", "get_rabbitmq", "init_connections", "close_connections"]


def get_config() -> Settings:
    """Get application settings."""
    return get_settings()


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Get Redis client connection."""
    global _redis_client
    settings = get_settings()

    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    try:
        yield _redis_client
    finally:
        pass  # Connection is managed globally


async def get_rabbitmq() -> AsyncGenerator[Connection, None]:
    """Get RabbitMQ connection."""
    global _rabbitmq_connection
    settings = get_settings()

    if _rabbitmq_connection is None or _rabbitmq_connection.is_closed:
        _rabbitmq_connection = await connect_robust(settings.rabbitmq_url)

    try:
        yield _rabbitmq_connection
    finally:
        pass  # Connection is managed globally


async def init_connections() -> None:
    """Initialize all external connections."""
    global _redis_client, _rabbitmq_connection
    settings = get_settings()

    # Initialize Redis
    _redis_client = redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )

    # Initialize RabbitMQ
    try:
        _rabbitmq_connection = await connect_robust(settings.rabbitmq_url)
    except Exception:
        # RabbitMQ connection is optional for basic functionality
        _rabbitmq_connection = None


async def close_connections() -> None:
    """Close all external connections."""
    global _redis_client, _rabbitmq_connection

    if _redis_client:
        await _redis_client.close()
        _redis_client = None

    if _rabbitmq_connection and not _rabbitmq_connection.is_closed:
        await _rabbitmq_connection.close()
        _rabbitmq_connection = None
