from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic import field_validator
from pydantic import ConfigDict
from datetime import datetime
from .source import SourceMetadata


class Query(BaseModel):
    """
    Represents a text query for semantic search
    """
    text: str = Field(..., description="The query text to be embedded and searched")
    top_k: Optional[int] = Field(default=5, ge=1, le=100, description="Number of top results to retrieve")
    similarity_threshold: Optional[float] = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity score for results")

    @field_validator('text')
    @classmethod
    def text_not_empty(cls, v):
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
            "text": "What is humanoid locomotion?",
            "top_k": 5,
            "similarity_threshold": 0.3
        }
    })


class QueryRequest(BaseModel):
    """
    Model representing a query request from the frontend
    """
    query: str = Field(..., description="The user's question", min_length=1, max_length=1000)
    context: Optional[str] = Field(None, description="Optional context from selected text", max_length=5000)
    sessionId: Optional[str] = Field(None, description="Optional session identifier for conversation history")
    userId: Optional[str] = Field(None, description="Optional user identifier")


class QueryResponse(BaseModel):
    """
    Model representing a response from the RAG system
    """
    response: str = Field(..., description="The AI-generated response")
    sources: List[SourceMetadata] = Field(..., description="Array of sources used to generate the response")
    sessionId: str = Field(..., description="Session identifier for conversation continuity")
    timestamp: str = Field(..., description="ISO date string for the response")