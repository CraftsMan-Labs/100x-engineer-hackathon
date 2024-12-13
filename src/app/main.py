import logging
from contextlib import asynccontextmanager
from typing import List
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Add project root to path
CUR_DIR = os.getcwd()
CUR_DIR = CUR_DIR.replace("\\", "/")
sys.path.append(CUR_DIR)
CUR_DIR = CUR_DIR + "/src"
sys.path.append(CUR_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import (
    market_expansion,
    product_evolution,
    market_analysis,
    customer_discovery,
    competitive_intelligence,
    chat
)
from app.db import Base, create_database_engine, create_session_factory
from app.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events
    """
    # Startup
    logger.info("Starting up Market Intelligence Platform...")
    try:
        # Initialize database
        engine = create_database_engine(settings.DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        
        # Create session factory
        session_factory = create_session_factory(engine)
        
        # Store in app state
        app.state.db_engine = engine
        app.state.session_factory = session_factory
        
        logger.info("Startup complete")
        yield
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    # Shutdown
    logger.info("Shutting down Market Intelligence Platform...")
    try:
        engine.dispose()
        logger.info("Shutdown complete")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Initialize FastAPI app
    app = FastAPI(
        title="Market Intelligence Platform",
        description="Comprehensive market research and business intelligence tool",
        version="0.1.0",
        lifespan=lifespan
    )

    # Configure CORS
    origins = [
        "http://localhost",
        "http://localhost:3000",  # React default port
        "http://localhost:8000",  # FastAPI default port
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    # Include routers
    app.include_router(market_expansion.router)
    app.include_router(product_evolution.router)
    app.include_router(market_analysis.router)
    app.include_router(customer_discovery.router)
    app.include_router(competitive_intelligence.router)
    app.include_router(chat.router)

    return app

# Create the application instance
app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
