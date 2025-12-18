from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from ...config.constants import MIN_QUERY_LENGTH, MAX_QUERY_LENGTH, MIN_SIMILARITY_THRESHOLD, MAX_SIMILARITY_THRESHOLD, MAX_TOP_K


class SearchRequest(BaseModel):
    """
    Request model for the search endpoint.
    Extends QueryRequest with API-specific fields.
    """
    query: str = Field(
        ...,
        description="The natural language query to search for",
        min_length=MIN_QUERY_LENGTH,
        max_length=MAX_QUERY_LENGTH,
        example="What are the benefits of renewable energy?"
    )
    top_k: int = Field(
        default=5,
        description="Number of results to return",
        ge=1,
        le=MAX_TOP_K,
        example=5
    )
    similarity_threshold: float = Field(
        default=0.5,
        description="Minimum similarity score for results",
        ge=MIN_SIMILARITY_THRESHOLD,
        le=MAX_SIMILARITY_THRESHOLD,
        example=0.5
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional filters for the search",
        example={"category": "science", "year": 2023}
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the request (for logging/tracing)",
        example="req_abc123"
    )

    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()

    @validator('similarity_threshold')
    def validate_similarity_threshold(cls, v):
        if not (MIN_SIMILARITY_THRESHOLD <= v <= MAX_SIMILARITY_THRESHOLD):
            raise ValueError(f'Similarity threshold must be between {MIN_SIMILARITY_THRESHOLD} and {MAX_SIMILARITY_THRESHOLD}')
        return v


class ValidateRequest(BaseModel):
    """
    Model for validation endpoint.
    """
    query: str = Field(
        ...,
        description="Query to validate",
        min_length=MIN_QUERY_LENGTH,
        max_length=MAX_QUERY_LENGTH,
        example="What are the benefits of renewable energy?"
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the request",
        example="req_def456"
    )

    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()