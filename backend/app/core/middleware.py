"""Middleware for the application."""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.
        
        Args:
            request: FastAPI request
            call_next: Next middleware
            
        Returns:
            Response
        """
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        
        logger.info(
            "request_started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        logger.info(
            "request_completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=f"{process_time:.3f}s",
        )
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


def setup_cors_middleware(app: any) -> None:
    """
    Setup CORS middleware.
    
    Args:
        app: FastAPI application
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
