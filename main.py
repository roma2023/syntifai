"""
Synthetic Data Generation Backend - Main Application Entry Point
==============================================================

This module serves as the FastAPI application entry point for the synthetic data generation system.
It initializes the web server, registers API routes, and configures OpenAPI documentation.

Architecture:
- FastAPI framework for REST API endpoints
- Uvicorn ASGI server for high-performance async handling
- Modular route organization via router inclusion
- OpenAPI/Swagger automatic documentation generation

Author: UBS syntifAI Team
Version: 0.0.1
"""

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════════════════════════

# Standard library imports
import sys
import os

# Add current directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), ''))

# Third-party imports
import uvicorn
from fastapi import FastAPI, Request

# Local imports
from route.restapi import router, config_data
from utils.logging_config import configure_logging, set_session, set_endpoint


# ═══════════════════════════════════════════════════════════════════════════════════════════════════
# APPLICATION CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════════════════════════

# OpenAPI documentation metadata
tags_metadata = [
    {
        "name": "Synthetic Generation",
        "description": "Allow user to perform `Synthetic data generation`."
    }
]

# API description for Swagger UI
description = """
**UBS syntifAI - Synthetic Data Generation Platform**

This API provides comprehensive synthetic data generation capabilities with:
- Database schema registration and management
- Natural language-driven data extraction
- Multi-table synthetic data generation with relationship preservation
- Advanced quality, diagnostic, and privacy analysis
- Session-based reporting and data archival

Built with FastAPI for high-performance async processing.
"""


# ═══════════════════════════════════════════════════════════════════════════════════════════════════
# APPLICATION INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════════════════════════

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application instance.
    
    Returns:
        FastAPI: Configured application instance
    """
    # Configure centralized logging once
    configure_logging()

    app = FastAPI(
        title="UBS syntifAI - Synthetic Data Generation API",
        description=description,
        version="0.0.1",
        openapi_tags=tags_metadata,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Register API routes
    app.include_router(router, prefix="", tags=["Synthetic Generation"])
    
    # Middleware to inject session_id and endpoint into logging context
    @app.middleware("http")
    async def logging_context_middleware(request: Request, call_next):
        try:
            session_id = request.headers.get("X-Session-Id") or request.query_params.get("session_id")
            set_session(session_id)
            set_endpoint(request.url.path)
            response = await call_next(request)
            return response
        finally:
            # Clear context for next request
            set_session(None)
            set_endpoint(None)
    
    return app


# Create application instance
app = create_app()


# ═══════════════════════════════════════════════════════════════════════════════════════════════════
# SERVER STARTUP
# ═══════════════════════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Application entry point for development server.
    
    Starts Uvicorn ASGI server with configuration from config.yaml:
    - Host and port settings
    - Optional SSL/TLS configuration for production
    - Auto-reload for development
    """
    uvicorn.run(
        "main:app",
        host=config_data.get("host", "0.0.0.0"),
        port=config_data.get("port", 80),
        reload=True,  # Enable auto-reload for development
        # ssl_keyfile="./localhost4-key.pem",    # Enable for HTTPS in production
        # ssl_certfile="./localhost4.pem"        # Enable for HTTPS in production
    )
