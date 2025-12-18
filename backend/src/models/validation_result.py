from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from .retrieval_result import RetrievalResult
from pydantic import ConfigDict


class ValidationResult(BaseModel):
    """
    Result of a validation test
    """
    test_id: str = Field(..., description="Identifier of the test case")
    query: str = Field(..., description="The test query")
    retrieved_results: List[RetrievalResult] = Field(..., description="Actual retrieved results")
    accuracy_score: float = Field(..., ge=0.0, le=1.0, description="Accuracy metric for the test")
    pass_validation: bool = Field(..., serialization_alias="pass", description="Whether the test passed")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional details about the test execution")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "test_id": "test-001",
            "query": "What is humanoid locomotion?",
            "retrieved_results": [
                {
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
            ],
            "accuracy_score": 0.88,
            "pass": True,
            "details": {
                "retrieved_chunk_ids": ["chunk-001", "chunk-002"],
                "expected_chunk_ids": ["chunk-001", "chunk-002", "chunk-003"],
                "precision": 0.85,
                "recall": 0.67,
                "f1_score": 0.75
            }
        }
    })