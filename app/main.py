"""
FastAPI application main entry point.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import close_db, init_db
from app.dependencies import close_connections, init_connections
from app.routers import health, items, users

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    try:
        await init_db()
    except Exception as e:
        if settings.debug:
            print(f"Warning: Database initialization failed: {e}")
    try:
        await init_connections()
    except Exception as e:
        if settings.debug:
            print(f"Warning: External connections initialization failed: {e}")
    yield
    # Shutdown
    await close_connections()
    await close_db()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="FastAPI Template with PostgreSQL, Redis, and RabbitMQ",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix=settings.api_prefix, tags=["Health"])
    app.include_router(users.router, prefix=settings.api_prefix, tags=["Users"])
    app.include_router(items.router, prefix=settings.api_prefix, tags=["Items"])

    return app


app = create_app()


@app.get("/")
async def root() -> dict:
    """Root endpoint with welcome message."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": f"{settings.api_prefix}/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
