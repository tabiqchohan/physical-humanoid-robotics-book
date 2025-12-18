from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from pydantic import field_validator
from pydantic import ConfigDict


class RetrievalRequest(BaseModel):
    """
    Request object for the retrieval API endpoint
    """
    query: str = Field(..., description="The search query text")
    top_k: Optional[int] = Field(default=5, ge=1, le=100, description="Number of results to return")
    similarity_threshold: Optional[float] = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity threshold")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters for metadata-based search")

    @field_validator('query')
    @classmethod
    def query_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Query text must not be empty or contain only whitespace')
        return v

    @field_validator('top_k')
    @classmethod
    def top_k_valid_range(cls, v):
        if v is not None and (v < 1 or v > 100):
            raise ValueError('top_k must be between 1 and 100')
        return v

    @field_validator('similarity_threshold')
    @classmethod
    def similarity_threshold_valid_range(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('similarity_threshold must be between 0.0 and 1.0')
        return v

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "query": "What is humanoid locomotion?",
            "top_k": 5,
            "similarity_threshold": 0.3,
            "filters": {"author": "John Doe"}
        }
    })