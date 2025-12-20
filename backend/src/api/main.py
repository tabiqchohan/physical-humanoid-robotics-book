from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys
from ..config.settings import settings
from ..config.constants import LOG_FORMAT
from ..services.logger_service import setup_logger


# Set up logging before creating the app
logging.basicConfig(level=getattr(logging, settings.log_level.upper()), format=LOG_FORMAT)
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    logger.info("Application starting up", extra={"environment": settings.environment})
    yield
    logger.info("Application shutting down", extra={"environment": settings.environment})


# Create the FastAPI application
app = FastAPI(
    title="RAG Chatbot Backend API",
    description="API for OpenAI Agent integration with RAG (Retrieval-Augmented Generation) functionality",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from .routes import health, retrieval
from . import chat

app.include_router(health.router, prefix="", tags=["health"])
app.include_router(retrieval.router, prefix="", tags=["retrieval"])
app.include_router(chat.router, prefix="", tags=["chat"])


# Health check endpoint is included via the health router
# Additional global configuration can be added here if needed