from pydantic import BaseModel, Field
from typing import Optional


class SourceMetadata(BaseModel):
    """
    Model representing metadata for a source used in RAG responses
    """
    title: str = Field(..., description="Title of the source document", max_length=200)
    url: str = Field(..., description="URL to the source location")
    content: str = Field(..., description="Relevant excerpt from the source", max_length=10000)
    score: float = Field(..., description="Relevance score from vector search", ge=0.0, le=1.0)
    page: Optional[int] = Field(None, description="Page number if applicable")