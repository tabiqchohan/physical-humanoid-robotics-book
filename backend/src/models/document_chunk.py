from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from pydantic import ConfigDict


class DocumentChunk(BaseModel):
    """
    Represents a chunk of a document stored in the vector database
    """
    chunk_id: str = Field(..., description="Unique identifier for the document chunk")
    content: str = Field(..., description="The actual text content of the chunk")
    url: str = Field(..., description="URL or source identifier for the original document")
    title: str = Field(..., description="Title of the document or section")
    section: str = Field(..., description="Section identifier within the document")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata fields")
    vector: Optional[list[float]] = Field(default=None, description="Embedding vector representation")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "chunk_id": "doc123-chunk456",
            "content": "This is the content of the document chunk...",
            "url": "https://example.com/document.pdf",
            "title": "Example Document",
            "section": "Introduction",
            "metadata": {"author": "John Doe", "year": 2023},
            "vector": [0.1, 0.2, 0.3, 0.4, 0.5]
        }
    })