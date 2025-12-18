import pytest
from fastapi.testclient import TestClient
from src.api.retrieval_api import app
from unittest.mock import patch, Mock
from src.models.document_chunk import DocumentChunk


# Create test client
client = TestClient(app)


class TestRetrievalAPI:
    """
    Integration tests for the retrieval API endpoints
    """

    @patch('src.api.retrieval_api.retrieval_service')
    def test_search_endpoint_success(self, mock_retrieval_service):
        """
        Test that the search endpoint returns correct response for valid request
        """
        # Mock the retrieval service
        mock_chunk = DocumentChunk(
            chunk_id="test-chunk",
            content="test content",
            url="http://example.com",
            title="Test Title",
            section="Test Section"
        )

        mock_result = Mock()
        mock_result.chunk = mock_chunk
        mock_result.similarity_score = 0.85
        mock_result.rank = 1

        mock_query_embedding = Mock()
        mock_query_embedding.text = "test query"
        mock_query_embedding.vector = [0.1, 0.2, 0.3]
        mock_query_embedding.model = "embed-english-v3.0"

        mock_retrieval_service.retrieve.return_value = (
            [mock_result],
            mock_query_embedding,
            100,
            125.5
        )

        # Make request
        response = client.post(
            "/retrieval/search",
            json={
                "query": "test query",
                "top_k": 5,
                "similarity_threshold": 0.3
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["query"] == "test query"
        assert len(data["results"]) == 1
        assert data["results"][0]["chunk"]["chunk_id"] == "test-chunk"
        assert data["results"][0]["similarity_score"] == 0.85
        assert data["results"][0]["rank"] == 1
        assert data["total_chunks_searched"] == 100
        assert data["execution_time_ms"] == 125.5

    @patch('src.api.retrieval_api.retrieval_service')
    def test_search_endpoint_with_filters(self, mock_retrieval_service):
        """
        Test that the search endpoint handles filters correctly
        """
        # Mock the retrieval service
        mock_chunk = DocumentChunk(
            chunk_id="test-chunk",
            content="test content",
            url="http://example.com",
            title="Test Title",
            section="Test Section"
        )

        mock_result = Mock()
        mock_result.chunk = mock_chunk
        mock_result.similarity_score = 0.90
        mock_result.rank = 1

        mock_query_embedding = Mock()
        mock_query_embedding.text = "filtered query"
        mock_query_embedding.vector = [0.1, 0.2, 0.3]
        mock_query_embedding.model = "embed-english-v3.0"

        mock_retrieval_service.retrieve.return_value = (
            [mock_result],
            mock_query_embedding,
            50,
            80.2
        )

        # Make request with filters
        response = client.post(
            "/retrieval/search",
            json={
                "query": "filtered query",
                "top_k": 3,
                "similarity_threshold": 0.5,
                "filters": {"author": "John Doe", "year": 2023}
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["query"] == "filtered query"
        assert len(data["results"]) == 1
        assert data["results"][0]["chunk"]["chunk_id"] == "test-chunk"
        assert data["results"][0]["similarity_score"] == 0.90
        assert data["total_chunks_searched"] == 50
        assert data["execution_time_ms"] == 80.2

    def test_search_endpoint_validation_error(self):
        """
        Test that the search endpoint returns 422 for invalid request
        """
        # Make request with invalid data (empty query)
        response = client.post(
            "/retrieval/search",
            json={
                "query": "",  # Empty query should fail validation
                "top_k": 5
            }
        )

        # Verify response is validation error
        assert response.status_code == 422

    def test_health_endpoint(self):
        """
        Test that the health endpoint returns correct response
        """
        # Make request
        response = client.get("/health")

        # Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "dependencies" in data
        assert "cohere" in data["dependencies"]
        assert "qdrant" in data["dependencies"]

    @patch('src.api.retrieval_api.retrieval_service')
    def test_search_endpoint_internal_error(self, mock_retrieval_service):
        """
        Test that the search endpoint returns 500 for internal errors
        """
        # Mock the retrieval service to raise an exception
        mock_retrieval_service.retrieve.side_effect = Exception("Internal error")

        # Make request
        response = client.post(
            "/retrieval/search",
            json={
                "query": "test query",
                "top_k": 5
            }
        )

        # Verify response is internal server error
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data