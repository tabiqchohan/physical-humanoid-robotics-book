from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from qdrant_client.http.models import PointStruct


class EmbeddingResult(BaseModel):
    """
    Internal model for embedding operations.
    """
    text: str = Field(
        ...,
        description="Original text that was embedded"
    )
    embedding: List[float] = Field(
        ...,
        description="The embedding vector"
    )
    model: str = Field(
        ...,
        description="The model used for embedding"
    )


class VectorSearchResult(BaseModel):
    """
    Internal model for vector search operations.
    """
    points: List[PointStruct] = Field(
        default_factory=list,
        description="Raw results from Qdrant"
    )
    query_embedding: List[float] = Field(
        ...,
        description="The query embedding used"
    )
    search_params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters used for the search"
    )


class RetrievedChunkInternal(BaseModel):
    """
    Internal model for a retrieved chunk, similar to the API model but for internal use.
    """
    id: str = Field(
        ...,
        description="Unique identifier for the chunk"
    )
    content: str = Field(
        ...,
        description="The actual text content of the chunk"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata associated with the chunk"
    )
    score: float = Field(
        ...,
        description="Similarity score between 0.0 and 1.0",
        ge=0.0,
        le=1.0
    )
    source: Optional[str] = Field(
        default=None,
        description="Source document identifier"
    )


class QueryRequestInternal(BaseModel):
    """
    Internal model for query requests with validation.
    """
    query: str = Field(
        ...,
        description="The natural language query text"
    )
    top_k: int = Field(
        default=5,
        description="Number of results to return",
        ge=1,
        le=100
    )
    similarity_threshold: float = Field(
        default=0.5,
        description="Minimum similarity score for results",
        ge=0.0,
        le=1.0
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional filters for the search"
    )

    def validate_query(self) -> None:
        """
        Validate the query parameters.
        """
        if not self.query or not self.query.strip():
            raise ValueError("Query cannot be empty")

        if not (1 <= self.top_k <= 100):
            raise ValueError("top_k must be between 1 and 100")

        if not (0.0 <= self.similarity_threshold <= 1.0):
            raise ValueError("similarity_threshold must be between 0.0 and 1.0")