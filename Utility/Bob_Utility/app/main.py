"""
FastAPI Application Entry Point
Enterprise Payload Utility Toolkit
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import xml_router, json_router, regex_router
from app.api.v1.endpoints.converter import router as converter_router
from app.api.v1.endpoints.security import router as security_router
from app.config import get_settings
from app.core.logger import setup_logging, get_logger

# Get settings
settings = get_settings()

# Setup logging
setup_logging(
    log_level=settings.log_level,
    log_format=settings.log_format,
    log_file=settings.log_file,
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API Documentation: http://{settings.backend_host}:{settings.backend_port}/docs")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.app_version,
    lifespan=lifespan,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Mount static files FIRST (before routes)
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(xml_router, prefix=settings.api_v1_prefix)
app.include_router(json_router, prefix=settings.api_v1_prefix)
app.include_router(regex_router, prefix=settings.api_v1_prefix)
app.include_router(converter_router, prefix=settings.api_v1_prefix)
app.include_router(security_router, prefix=settings.api_v1_prefix)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - Split Pane UI"""
    static_dir = Path(__file__).parent / "static"
    split_pane_ui_path = static_dir / "split-pane-ui.html"
    
    if split_pane_ui_path.exists():
        return FileResponse(
            split_pane_ui_path,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    
    return HTMLResponse("<h1>Enterprise Payload Utility Toolkit</h1><p>UI file not found</p>")


@app.get("/modern", response_class=HTMLResponse)
async def modern_ui():
    """Alternate modern UI with tabs"""
    static_dir = Path(__file__).parent / "static"
    modern_ui_path = static_dir / "modern-ui.html"
    
    if modern_ui_path.exists():
        return FileResponse(modern_ui_path)
    
    return HTMLResponse("<h1>Modern UI</h1><p>UI file not found</p>")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.app_version}


@app.get("/static/favicon.svg")
async def favicon():
    """Serve favicon"""
    static_dir = Path(__file__).parent / "static"
    favicon_path = static_dir / "favicon.svg"
    
    if favicon_path.exists():
        return FileResponse(favicon_path, media_type="image/svg+xml")
    
    return HTMLResponse("<svg></svg>", media_type="image/svg+xml")

# Made with Bob
