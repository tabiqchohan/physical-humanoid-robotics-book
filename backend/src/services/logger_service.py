import logging
import json
from typing import Dict, Any, Optional
from contextvars import ContextVar
from pythonjsonlogger import jsonlogger
from ..config.settings import settings


# Context variable to store correlation ID
correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter that adds correlation ID to log entries.
    """
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

        # Add correlation ID if available
        correlation_id = correlation_id_var.get()
        if correlation_id:
            log_record['correlation_id'] = correlation_id


def setup_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with JSON formatting and correlation ID support.

    Args:
        name: Name of the logger
        log_level: Log level (uses settings if not provided)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Set log level
    level = getattr(logging, log_level or settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Prevent adding multiple handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = CustomJsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def set_correlation_id(correlation_id: str) -> None:
    """
    Set the correlation ID for the current context.

    Args:
        correlation_id: The correlation ID to set
    """
    correlation_id_var.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """
    Get the correlation ID for the current context.

    Returns:
        The current correlation ID or None
    """
    return correlation_id_var.get()


def log_api_request(
    logger: logging.Logger,
    request_id: str,
    endpoint: str,
    method: str,
    processing_time: float,
    status_code: int,
    user_agent: Optional[str] = None,
    ip_address: Optional[str] = None
) -> None:
    """
    Log an API request with structured data.

    Args:
        logger: Logger instance to use
        request_id: Unique request identifier
        endpoint: API endpoint that was called
        method: HTTP method used
        processing_time: Time taken to process the request in seconds
        status_code: HTTP status code returned
        user_agent: User agent string (if available)
        ip_address: Client IP address (if available)
    """
    logger.info(
        "API request processed",
        extra={
            "request_id": request_id,
            "endpoint": endpoint,
            "method": method,
            "processing_time": processing_time,
            "status_code": status_code,
            "user_agent": user_agent,
            "ip_address": ip_address
        }
    )


def log_retrieval_request(
    logger: logging.Logger,
    request_id: str,
    query: str,
    top_k: int,
    similarity_threshold: float,
    num_results: int,
    processing_time: float
) -> None:
    """
    Log a retrieval request with structured data.

    Args:
        logger: Logger instance to use
        request_id: Unique request identifier
        query: The query that was processed
        top_k: Number of results requested
        similarity_threshold: Similarity threshold used
        num_results: Number of results returned
        processing_time: Time taken to process the request in seconds
    """
    logger.info(
        "Retrieval request processed",
        extra={
            "request_id": request_id,
            "query": query,
            "top_k": top_k,
            "similarity_threshold": similarity_threshold,
            "num_results": num_results,
            "processing_time": processing_time
        }
    )


def log_error(
    logger: logging.Logger,
    error_type: str,
    error_message: str,
    request_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log an error with structured data.

    Args:
        logger: Logger instance to use
        error_type: Type of error that occurred
        error_message: Error message
        request_id: Associated request ID (if applicable)
        details: Additional error details
    """
    logger.error(
        error_message,
        extra={
            "error_type": error_type,
            "request_id": request_id,
            "details": details or {}
        }
    )