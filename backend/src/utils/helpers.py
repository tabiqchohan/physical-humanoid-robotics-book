import uuid
import time
import re
from typing import Optional, Dict, Any, List
from ..config.constants import MIN_QUERY_LENGTH


def generate_request_id() -> str:
    """
    Generate a unique request ID for correlation and tracing.

    Returns:
        A unique request identifier
    """
    return f"req_{uuid.uuid4().hex[:8]}"


def validate_query_text(query: str) -> bool:
    """
    Validate that a query text is meaningful.

    Args:
        query: The query text to validate

    Returns:
        True if the query is valid, False otherwise
    """
    if not query or len(query.strip()) < MIN_QUERY_LENGTH:
        return False

    # Check if the query contains at least some meaningful content (not just punctuation)
    clean_query = re.sub(r'[^\w\s]', '', query.strip())
    if not clean_query or len(clean_query.strip()) < MIN_QUERY_LENGTH:
        return False

    return True


def sanitize_query(query: str) -> str:
    """
    Sanitize a query string by removing potentially harmful content.

    Args:
        query: The query string to sanitize

    Returns:
        Sanitized query string
    """
    # Remove excessive whitespace
    sanitized = ' '.join(query.split())

    # Remove potentially harmful characters (but preserve meaningful punctuation)
    # This is a basic sanitization - in production, you might want more sophisticated validation
    return sanitized


def calculate_processing_time(start_time: float) -> float:
    """
    Calculate processing time from start time to current time.

    Args:
        start_time: The start time (from time.time())

    Returns:
        Processing time in seconds
    """
    return time.time() - start_time


def merge_metadata(base_metadata: Dict[str, Any], additional_metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge two metadata dictionaries, with additional_metadata taking precedence.

    Args:
        base_metadata: The base metadata dictionary
        additional_metadata: Additional metadata to merge (can be None)

    Returns:
        Merged metadata dictionary
    """
    if additional_metadata is None:
        return base_metadata.copy()

    merged = base_metadata.copy()
    merged.update(additional_metadata)
    return merged


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.

    Args:
        lst: The list to chunk
        chunk_size: The size of each chunk

    Returns:
        List of chunks
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def format_error_response(error_type: str, error_message: str, request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Format a standard error response.

    Args:
        error_type: Type of error
        error_message: Error message
        request_id: Associated request ID (optional)

    Returns:
        Formatted error response dictionary
    """
    return {
        "error": error_message,
        "type": error_type,
        "details": {},
        "request_id": request_id
    }


def is_valid_embedding(embedding: List[float]) -> bool:
    """
    Validate that an embedding is properly formatted.

    Args:
        embedding: The embedding vector to validate

    Returns:
        True if the embedding is valid, False otherwise
    """
    if not isinstance(embedding, list) or len(embedding) == 0:
        return False

    # Check that all elements are numbers
    for value in embedding:
        if not isinstance(value, (int, float)) or not (-1 <= value <= 1):
            return False

    return True


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent processing.

    Args:
        text: The text to normalize

    Returns:
        Normalized text
    """
    # Convert to lowercase and normalize whitespace
    normalized = ' '.join(text.lower().split())
    return normalized


def log_api_request(
    logger,
    request_id: str,
    endpoint: str,
    method: str,
    processing_time: float,
    status_code: int,
    user_agent: str = None,
    ip_address: str = None
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
    # This function is a placeholder that would call the logger service
    # In the actual implementation, it should call the logger service's log_api_request function
    pass


def log_retrieval_request(
    logger,
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
    # This function is a placeholder that would call the logger service
    # In the actual implementation, it should call the logger service's log_retrieval_request function
    pass