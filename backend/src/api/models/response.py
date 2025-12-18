from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from ...config.constants import PROCESSING_STATUS_SUCCESS, PROCESSING_STATUS_PARTIAL, PROCESSING_STATUS_ERROR


class RetrievedChunk(BaseModel):
    """
    Represents a segment of text retrieved from the knowledge base, including content, metadata, and relevance score.
    """
    id: str = Field(
        ...,
        description="Unique identifier for the chunk",
        example="doc_123"
    )
    content: str = Field(
        ...,
        description="The actual text content of the chunk",
        example="Renewable energy sources like solar and wind power provide clean alternatives..."
    )
    metadata: Dict[str, Any] = Field(
        ...,
        description="Additional metadata associated with the chunk",
        example={"source": "energy_report.pdf", "page": 15, "author": "John Doe"}
    )
    score: float = Field(
        ...,
        description="Similarity score between 0.0 and 1.0",
        ge=0.0,
        le=1.0,
        example=0.87
    )
    source: Optional[str] = Field(
        default=None,
        description="Source document identifier",
        example="energy_report.pdf"
    )


class RetrievalResponse(BaseModel):
    """
    Structured response containing retrieved document chunks and metadata.
    """
    query: str = Field(
        ...,
        description="The original query that was processed",
        example="What are the benefits of renewable energy?"
    )
    results: List[RetrievedChunk] = Field(
        default_factory=list,
        description="List of relevant document chunks"
    )
    total_results: int = Field(
        ...,
        description="Total number of results found before filtering",
        example=1
    )
    processing_time: float = Field(
        ...,
        description="Time taken to process the request in seconds",
        ge=0,
        example=0.123
    )
    query_embedding: Optional[List[float]] = Field(
        default=None,
        description="The embedding vector of the query (optional)",
        example=[0.1, 0.3, 0.5, 0.7]
    )


class SearchResponse(RetrievalResponse):
    """
    Extends RetrievalResponse with API-specific fields.
    """
    request_id: str = Field(
        ...,
        description="Request identifier for correlation",
        example="req_abc123"
    )
    status: str = Field(
        default=PROCESSING_STATUS_SUCCESS,
        description="Status of the request",
        example="success"
    )


class ValidateResponse(BaseModel):
    """
    Model for validation endpoint response.
    """
    request_id: str = Field(
        ...,
        description="Request identifier for correlation",
        example="req_def456"
    )
    is_valid: bool = Field(
        ...,
        description="Whether the query is valid",
        example=True
    )
    message: str = Field(
        ...,
        description="Validation message",
        example="Query is valid and can be processed"
    )
    suggestions: Optional[List[str]] = Field(
        default=None,
        description="Suggestions for improving the query",
        example=["Consider adding more specific terms", "Try using synonyms"]
    )


class ValidationError(BaseModel):
    """
    Represents an error that occurred during request validation.
    """
    error: str = Field(
        ...,
        description="Error message",
        example="Query cannot be empty"
    )
    field: Optional[str] = Field(
        default=None,
        description="Field that caused the error (if applicable)",
        example="query"
    )


class ServiceError(BaseModel):
    """
    Represents an error that occurred during service processing.
    """
    error: str = Field(
        ...,
        description="Error message",
        example="Failed to connect to vector database"
    )
    type: str = Field(
        ...,
        description="Type of error",
        example="database_error"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details",
        example={"connection_timeout": 30}
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Request identifier for correlation",
        example="req_ghi789"
    )


class ErrorResponse(BaseModel):
    """
    Standard error response model for API endpoints.
    """
    error: str = Field(
        ...,
        description="Error message",
        example="Invalid query parameters"
    )
    type: str = Field(
        default="validation_error",
        description="Type of error",
        example="validation_error"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details",
        example={"field": "query", "reason": "query cannot be empty"}
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Request identifier for correlation",
        example="req_ghi789"
    )


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    """
    status: str = Field(
        ...,
        description="Service health status",
        example="healthy"
    )
    timestamp: str = Field(
        ...,
        description="Timestamp of the health check",
        example="2025-12-17T10:30:00Z"
    )
    version: Optional[str] = Field(
        default=None,
        description="Service version",
        example="1.0.0"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional health check details",
        example={"database": "connected", "cohere": "available"}
    )