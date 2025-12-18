from pydantic import BaseModel, Field
from typing import List
from .retrieval_result import RetrievalResult
from pydantic import ConfigDict


class RetrievalResponse(BaseModel):
    """
    Response object from the retrieval API endpoint
    """
    query: str = Field(..., description="The original query text")
    results: List[RetrievalResult] = Field(..., description="Ranked list of retrieval results")
    total_chunks_searched: int = Field(..., description="Total number of chunks considered")
    execution_time_ms: float = Field(..., description="Time taken for the retrieval operation")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "query": "What is humanoid locomotion?",
            "results": [
                {
                    "chunk": {
                        "chunk_id": "doc123-chunk456",
                        "content": "This is the content of the document chunk...",
                        "url": "https://example.com/document.pdf",
                        "title": "Example Document",
                        "section": "Introduction"
                    },
                    "similarity_score": 0.85,
                    "rank": 1
                }
            ],
            "total_chunks_searched": 100,
            "execution_time_ms": 125.5
        }
    })
