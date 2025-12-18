from fastapi import APIRouter, HTTPException
from typing import Dict
from datetime import datetime
import logging

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)


@router.get("/health", response_model=Dict)
async def health_check():
    """
    Check the health of the RAG system
    """
    try:
        # In a real implementation, you might check connections to external services
        # like the vector database, Cohere API, etc.

        health_status = {
            "status": "healthy",
            "backend": "available",
            "vector_db": "connected",  # This would be checked in a real implementation
            "timestamp": datetime.now().isoformat()
        }

        logger.info("Health check performed successfully")
        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")