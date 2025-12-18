from fastapi import APIRouter, Depends
from datetime import datetime
from ...config.settings import settings
from ...config.constants import CORRELATION_ID_HEADER
from ...api.models.response import HealthResponse
from ...services.logger_service import setup_logger, get_correlation_id
from ...utils.helpers import generate_request_id
import uuid


router = APIRouter()
logger = setup_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify that the service is running and healthy.
    """
    request_id = generate_request_id()

    # Set correlation ID for this request
    # Note: In a real implementation with middleware, this would be handled automatically
    # For now, we're setting it here for logging purposes

    try:
        # In a real implementation, you might want to check connectivity to dependencies
        # like the vector database or Cohere API here
        health_status = "healthy"
        timestamp = datetime.utcnow().isoformat() + "Z"

        response = HealthResponse(
            status=health_status,
            timestamp=timestamp,
            version=settings.app_version if hasattr(settings, 'app_version') else "1.0.0"
        )

        logger.info(
            "Health check performed",
            extra={
                "request_id": request_id,
                "status": health_status,
                "timestamp": timestamp
            }
        )

        return response
    except Exception as e:
        logger.error(
            "Health check failed",
            extra={
                "request_id": request_id,
                "error": str(e)
            }
        )
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow().isoformat() + "Z",
            details={"error": str(e)}
        )


@router.get("/ready", response_model=HealthResponse)
async def readiness_check():
    """
    Readiness check endpoint to verify that the service is ready to accept traffic.
    """
    request_id = generate_request_id()

    try:
        # Check if all required services are available
        # This is a basic implementation - in production you'd check actual dependencies
        ready_status = "ready"
        timestamp = datetime.utcnow().isoformat() + "Z"

        response = HealthResponse(
            status=ready_status,
            timestamp=timestamp
        )

        logger.info(
            "Readiness check performed",
            extra={
                "request_id": request_id,
                "status": ready_status,
                "timestamp": timestamp
            }
        )

        return response
    except Exception as e:
        logger.error(
            "Readiness check failed",
            extra={
                "request_id": request_id,
                "error": str(e)
            }
        )
        return HealthResponse(
            status="not ready",
            timestamp=datetime.utcnow().isoformat() + "Z",
            details={"error": str(e)}
        )