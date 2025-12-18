from pydantic import BaseModel, Field
from typing import Optional
from .document_chunk import DocumentChunk
from pydantic import field_validator
from pydantic import ConfigDict


class RetrievalResult(BaseModel):
    """
    Represents a single result from the retrieval operation
    """
    chunk: DocumentChunk = Field(..., description="The retrieved document chunk")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity score between query and chunk")
    rank: int = Field(..., ge=1, description="Position in the ranked results (1-indexed)")

    @field_validator('similarity_score')
    @classmethod
    def similarity_score_valid_range(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError('similarity_score must be between 0.0 and 1.0')
        return v

    @field_validator('rank')
    @classmethod
    def rank_positive(cls, v):
        if v < 1:
            raise ValueError('rank must be a positive integer')
        return v

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "chunk": {
                "chunk_id": "doc123-chunk456",
                "content": "This is the content of the document chunk...",
                "url": "https://example.com/document.pdf",
                "title": "Example Document",
                "section": "Introduction",
                "metadata": {"author": "John Doe", "year": 2023}
            },
            "similarity_score": 0.85,
            "rank": 1
        }
    })