"""Main FastAPI application."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.redis import RedisClient
from app.core.logging import setup_logging, logger
from app.core.middleware import RequestLoggingMiddleware, setup_cors_middleware
from app.core.exceptions import PortfelException
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Args:
        app: FastAPI application
    """
    # Startup
    setup_logging()
    logger.info("Starting application", app_name=settings.APP_NAME, version=settings.APP_VERSION)
    
    # Initialize database (optional - using Alembic instead)
    # await init_db()
    
    # Initialize Redis
    await RedisClient.get_client()
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await close_db()
    await RedisClient.close()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Financial Management System",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Setup CORS
setup_cors_middleware(app)

# Add custom middleware
app.add_middleware(RequestLoggingMiddleware)

# Include routers
app.include_router(api_router, prefix=settings.API_PREFIX)


# Exception handlers
@app.exception_handler(PortfelException)
async def portfel_exception_handler(request: Request, exc: PortfelException) -> JSONResponse:
    """Handle custom application exceptions."""
    logger.error(
        "Application exception",
        exception=exc.__class__.__name__,
        message=exc.message,
        status_code=exc.status_code,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation errors."""
    logger.warning(
        "Validation error",
        errors=exc.errors(),
        path=request.url.path,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
