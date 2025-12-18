import pytest
from fastapi.testclient import TestClient
from src.api.retrieval_api import app
from unittest.mock import patch, Mock
from src.models.document_chunk import DocumentChunk
from src.models.retrieval_result import RetrievalResult


# Create test client
client = TestClient(app)


class TestValidationAPI:
    """
    Integration tests for the validation API endpoints
    """

    @patch('src.api.retrieval_api.validation_service')
    def test_validate_endpoint_success(self, mock_validation_service):
        """
        Test that the validate endpoint returns correct response for valid request
        """
        # Mock the validation service
        mock_chunk = DocumentChunk(
            chunk_id="test-chunk-1",
            content="test content 1",
            url="http://example.com/1",
            title="Test Title 1",
            section="Test Section 1"
        )

        mock_result = Mock()
        mock_result.chunk = mock_chunk
        mock_result.similarity_score = 0.85
        mock_result.rank = 1

        mock_validation_result = Mock()
        mock_validation_result.test_id = "test-001"
        mock_validation_result.query = "test validation query"
        mock_validation_result.retrieved_results = [mock_result]
        mock_validation_result.accuracy_score = 0.88
        mock_validation_result.pass_validation = True
        mock_validation_result.details = {
            "retrieved_chunk_ids": ["test-chunk-1"],
            "expected_chunk_ids": ["test-chunk-1", "test-chunk-2"],
            "precision": 0.85,
            "recall": 0.67,
            "f1_score": 0.75,
            "execution_time_ms": 150.0
        }

        mock_validation_service.run_validation_test.return_value = mock_validation_result

        # Make request
        response = client.post(
            "/retrieval/validate",
            json={
                "test_id": "test-001",
                "query": "test validation query",
                "expected_chunks": ["test-chunk-1", "test-chunk-2"],
                "expected_keywords": ["test", "validation"],
                "top_k": 5,
                "similarity_threshold": 0.3
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["test_id"] == "test-001"
        assert data["query"] == "test validation query"
        assert len(data["retrieved_results"]) == 1
        assert data["retrieved_results"][0]["chunk"]["chunk_id"] == "test-chunk-1"
        assert data["accuracy_score"] == 0.88
        assert data["pass"] is True
        assert "details" in data
        assert data["details"]["precision"] == 0.85

    def test_validate_endpoint_validation_error(self):
        """
        Test that the validate endpoint returns 422 for invalid request
        """
        # Make request with invalid data (empty test_id)
        response = client.post(
            "/retrieval/validate",
            json={
                "test_id": "",  # Empty test_id should fail validation
                "query": "test query",
                "expected_chunks": []
            }
        )

        # Verify response is validation error
        assert response.status_code == 422

    @patch('src.api.retrieval_api.validation_service')
    def test_validate_endpoint_internal_error(self, mock_validation_service):
        """
        Test that the validate endpoint returns 500 for internal errors
        """
        # Mock the validation service to raise an exception
        mock_validation_service.run_validation_test.side_effect = Exception("Internal error")

        # Make request
        response = client.post(
            "/retrieval/validate",
            json={
                "test_id": "test-001",
                "query": "test validation query",
                "expected_chunks": ["chunk-1"]
            }
        )

        # Verify response is internal server error
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data