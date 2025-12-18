from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from pydantic import ConfigDict


class ValidationTest(BaseModel):
    """
    Represents a validation test case for the retrieval pipeline
    """
    test_id: str = Field(..., min_length=1, description="Unique identifier for the test")
    query: str = Field(..., min_length=1, description="The test query")
    expected_chunks: List[str] = Field(..., description="Expected chunk IDs")
    expected_keywords: Optional[List[str]] = Field(default=None, description="Keywords expected in results")
    metadata_filters: Optional[Dict[str, Any]] = Field(default=None, description="Filters to apply during test")
    top_k: Optional[int] = Field(default=5, ge=1, le=100, description="Number of results to return")
    similarity_threshold: Optional[float] = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity threshold")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "test_id": "test-001",
            "query": "What is humanoid locomotion?",
            "expected_chunks": ["chunk-001", "chunk-002", "chunk-003"],
            "expected_keywords": ["locomotion", "humanoid", "movement"],
            "metadata_filters": {"author": "John Doe"},
            "top_k": 5,
            "similarity_threshold": 0.3
        }
    })