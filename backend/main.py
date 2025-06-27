from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .app.database import connect_to_mongo, close_mongo_connection
from .app.routes.question import router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info("Starting up application...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("Shutting down application...")
    await close_mongo_connection()


app = FastAPI(
    title="Crewmind.ai Assistant API",
    description="A simple AI assistant backend with MongoDB storage",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # React dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["questions"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Crewmind.ai Assistant API is running!", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {"status": "healthy", "service": "crewmind-ai-backend", "version": "1.0.0"}
