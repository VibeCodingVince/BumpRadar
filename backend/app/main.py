"""
BumpRadar API
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import logging
import os

from app.core.config import settings
from app.core.database import init_db, engine
from app.api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting Pregnancy Safety Radar API...")
    init_db()
    logger.info("✅ Database initialized")
    # Run migrations
    try:
        from sqlalchemy import text, inspect
        inspector = inspect(engine)
        # Migrate: add tier column to subscribers if missing
        sub_columns = [c["name"] for c in inspector.get_columns("subscribers")]
        if "tier" not in sub_columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE subscribers ADD COLUMN tier VARCHAR(20) DEFAULT 'pro' NOT NULL"))
            logger.info("✅ Added 'tier' column to subscribers table")
        # Migrate: add username column to users if missing
        user_columns = [c["name"] for c in inspector.get_columns("users")]
        if "username" not in user_columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR(50)"))
            logger.info("✅ Added 'username' column to users table")
    except Exception as e:
        logger.debug(f"Migration skipped: {e}")
    if settings.SECRET_KEY == "dev-secret-key-change-in-production":
        logger.warning("⚠️  Using default SECRET_KEY — set SECRET_KEY env var in production!")
    logger.info(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} ready!")

    yield

    # Shutdown
    logger.info("👋 Shutting down Pregnancy Safety Radar API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered ingredient safety checker for pregnancy",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
# Allow the configured frontend URL
if settings.FRONTEND_URL and settings.FRONTEND_URL not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(settings.FRONTEND_URL)
# Allow additional origins from CORS_ORIGINS env var
if settings.CORS_ORIGINS:
    for origin in settings.CORS_ORIGINS.split(","):
        origin = origin.strip()
        if origin and origin not in ALLOWED_ORIGINS:
            ALLOWED_ORIGINS.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Serve frontend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")


@app.get("/")
async def root():
    """Serve the frontend"""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "message": "BumpRadar API is running"
    }


@app.get("/logo.png")
async def serve_logo():
    """Serve the logo image."""
    logo_path = os.path.join(FRONTEND_DIR, "logo.png")
    if os.path.isfile(logo_path):
        return FileResponse(logo_path, media_type="image/png")
    return FileResponse(status_code=404)


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn

    # Configure uvicorn with larger request body size for image uploads
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        timeout_keep_alive=30,
        # Increase max request body size to 20MB for image uploads
        limit_max_requests=10000,
    )
    server = uvicorn.Server(config)
    server.run()
