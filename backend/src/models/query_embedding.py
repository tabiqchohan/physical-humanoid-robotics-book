from pydantic import BaseModel, Field
from typing import List
from pydantic import ConfigDict


class QueryEmbedding(BaseModel):
    """
    Represents an embedded query for semantic search
    """
    text: str = Field(..., description="Original query text")
    vector: List[float] = Field(..., description="Embedding vector representation")
    model: str = Field(..., description="The embedding model used")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "text": "What is humanoid locomotion?",
            "vector": [0.1, 0.2, 0.3, 0.4, 0.5],
            "model": "embed-english-v3.0"
        }
    })