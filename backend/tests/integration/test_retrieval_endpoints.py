import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from src.api.main import app
from src.services.models import RetrievedChunkInternal


def test_search_endpoint_success():
    """
    Test successful search endpoint request.
    """
    client = TestClient(app)

    # Mock the retrieval service
    with patch('src.api.routes.retrieval.get_retrieval_service') as mock_service_getter:
        mock_service = MagicMock()
        mock_service_getter.return_value = mock_service

        # Mock the retrieve method
        mock_chunks = [
            RetrievedChunkInternal(
                id="chunk1",
                content="Test content 1",
                metadata={"source": "doc1.pdf", "page": 1},
                score=0.85,
                source="doc1.pdf"
            )
        ]
        mock_embedding = [0.1, 0.2, 0.3, 0.4]
        mock_processing_time = 0.123

        mock_service.retrieve = AsyncMock(return_value=(mock_chunks, mock_embedding, mock_processing_time))
        mock_service.convert_internal_chunks_to_api_response = MagicMock(
            return_value=[
                {
                    "id": "chunk1",
                    "content": "Test content 1",
                    "metadata": {"source": "doc1.pdf", "page": 1},
                    "score": 0.85,
                    "source": "doc1.pdf"
                }
            ]
        )

        # Make request
        response = client.post(
            "/retrieval/search",
            json={
                "query": "What are the benefits of renewable energy?",
                "top_k": 3,
                "similarity_threshold": 0.5
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["query"] == "What are the benefits of renewable energy?"
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == "chunk1"
        assert data["results"][0]["content"] == "Test content 1"
        assert data["results"][0]["score"] == 0.85
        assert data["total_results"] == 1
        assert data["processing_time"] == mock_processing_time
        assert data["request_id"] is not None
        assert data["status"] == "success"


def test_search_endpoint_with_filters():
    """
    Test search endpoint with filters.
    """
    client = TestClient(app)

    # Mock the retrieval service
    with patch('src.api.routes.retrieval.get_retrieval_service') as mock_service_getter:
        mock_service = MagicMock()
        mock_service_getter.return_value = mock_service

        # Mock the retrieve method
        mock_chunks = [
            RetrievedChunkInternal(
                id="chunk2",
                content="Filtered test content",
                metadata={"source": "doc2.pdf", "category": "science"},
                score=0.90,
                source="doc2.pdf"
            )
        ]
        mock_embedding = [0.5, 0.6, 0.7, 0.8]
        mock_processing_time = 0.098

        mock_service.retrieve = AsyncMock(return_value=(mock_chunks, mock_embedding, mock_processing_time))
        mock_service.convert_internal_chunks_to_api_response = MagicMock(
            return_value=[
                {
                    "id": "chunk2",
                    "content": "Filtered test content",
                    "metadata": {"source": "doc2.pdf", "category": "science"},
                    "score": 0.90,
                    "source": "doc2.pdf"
                }
            ]
        )

        # Make request with filters
        response = client.post(
            "/retrieval/search",
            json={
                "query": "science topic",
                "top_k": 5,
                "similarity_threshold": 0.6,
                "filters": {"category": "science", "year": 2023}
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["query"] == "science topic"
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == "chunk2"
        assert data["results"][0]["content"] == "Filtered test content"
        assert data["results"][0]["score"] == 0.90
        assert data["total_results"] == 1


def test_search_endpoint_validation_error():
    """
    Test search endpoint with validation error (empty query).
    """
    client = TestClient(app)

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
    data = response.json()
    assert "detail" in data


def test_validate_endpoint_success():
    """
    Test successful validate endpoint request.
    """
    client = TestClient(app)

    # Mock the retrieval service
    with patch('src.api.routes.retrieval.get_retrieval_service') as mock_service_getter:
        mock_service = MagicMock()
        mock_service_getter.return_value = mock_service

        # Mock the validate_query method
        mock_validation_result = {
            "is_valid": True,
            "message": "Query is valid and can be processed",
            "suggestions": None
        }

        mock_service.validate_query = AsyncMock(return_value=mock_validation_result)

        # Make request
        response = client.post(
            "/retrieval/validate",
            json={
                "query": "Is renewable energy beneficial?"
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["is_valid"] is True
        assert data["message"] == "Query is valid and can be processed"
        assert data["suggestions"] is None
        assert data["request_id"] is not None


def test_validate_endpoint_invalid_query():
    """
    Test validate endpoint with invalid query.
    """
    client = TestClient(app)

    # Mock the retrieval service
    with patch('src.api.routes.retrieval.get_retrieval_service') as mock_service_getter:
        mock_service = MagicMock()
        mock_service_getter.return_value = mock_service

        # Mock the validate_query method
        mock_validation_result = {
            "is_valid": False,
            "message": "Query cannot be empty",
            "suggestions": ["Provide a non-empty query"]
        }

        mock_service.validate_query = AsyncMock(return_value=mock_validation_result)

        # Make request with empty query
        response = client.post(
            "/retrieval/validate",
            json={
                "query": ""
            }
        )

        # Verify response
        assert response.status_code == 200  # Validation endpoint should return 200 even for invalid queries
        data = response.json()

        assert data["is_valid"] is False
        assert data["message"] == "Query cannot be empty"
        assert data["suggestions"] == ["Provide a non-empty query"]
        assert data["request_id"] is not None


def test_health_endpoint():
    """
    Test health endpoint returns correct response.
    """
    client = TestClient(app)

    # Make request
    response = client.get("/health")

    # Verify response
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_search_endpoint_internal_error():
    """
    Test search endpoint with internal error.
    """
    client = TestClient(app)

    # Mock the retrieval service to raise an exception
    with patch('src.api.routes.retrieval.get_retrieval_service') as mock_service_getter:
        mock_service = MagicMock()
        mock_service_getter.return_value = mock_service

        mock_service.retrieve.side_effect = Exception("Internal error")

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


def test_search_endpoint_ranked_results():
    """
    Test scenario 1: Query with relevant keywords returns ranked results.
    """
    client = TestClient(app)

    # Mock the retrieval service
    with patch('src.api.routes.retrieval.get_retrieval_service') as mock_service_getter:
        mock_service = MagicMock()
        mock_service_getter.return_value = mock_service

        # Mock the retrieve method with multiple results that should be ranked by score
        mock_chunks = [
            RetrievedChunkInternal(
                id="chunk-high",
                content="This document has high relevance to renewable energy benefits",
                metadata={"source": "doc1.pdf"},
                score=0.95,
                source="doc1.pdf"
            ),
            RetrievedChunkInternal(
                id="chunk-medium",
                content="This document somewhat relates to renewable energy",
                metadata={"source": "doc2.pdf"},
                score=0.75,
                source="doc2.pdf"
            ),
            RetrievedChunkInternal(
                id="chunk-low",
                content="This document has minimal relation to the topic",
                metadata={"source": "doc3.pdf"},
                score=0.60,
                source="doc3.pdf"
            )
        ]
        mock_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_processing_time = 0.150

        mock_service.retrieve = AsyncMock(return_value=(mock_chunks, mock_embedding, mock_processing_time))
        mock_service.convert_internal_chunks_to_api_response = MagicMock(
            return_value=[
                {
                    "id": "chunk-high",
                    "content": "This document has high relevance to renewable energy benefits",
                    "metadata": {"source": "doc1.pdf"},
                    "score": 0.95,
                    "source": "doc1.pdf"
                },
                {
                    "id": "chunk-medium",
                    "content": "This document somewhat relates to renewable energy",
                    "metadata": {"source": "doc2.pdf"},
                    "score": 0.75,
                    "source": "doc2.pdf"
                },
                {
                    "id": "chunk-low",
                    "content": "This document has minimal relation to the topic",
                    "metadata": {"source": "doc3.pdf"},
                    "score": 0.60,
                    "source": "doc3.pdf"
                }
            ]
        )

        # Make request with a query that should match the content
        response = client.post(
            "/retrieval/search",
            json={
                "query": "What are the benefits of renewable energy?",
                "top_k": 5
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        # Check that we got results
        assert len(data["results"]) == 3

        # Check that results are ranked by score (highest first)
        assert data["results"][0]["score"] >= data["results"][1]["score"]
        assert data["results"][1]["score"] >= data["results"][2]["score"]
        assert data["results"][0]["score"] == 0.95  # Highest score first
        assert data["results"][2]["score"] == 0.60  # Lowest score last

        # Check that the content is relevant to the query
        assert "renewable energy" in data["results"][0]["content"].lower()
        assert "renewable energy" in data["results"][1]["content"].lower()


def test_search_endpoint_no_matches():
    """
    Test scenario 2: Query with no relevant matches in the database returns empty or minimal results.
    """
    client = TestClient(app)

    # Mock the retrieval service
    with patch('src.api.routes.retrieval.get_retrieval_service') as mock_service_getter:
        mock_service = MagicMock()
        mock_service_getter.return_value = mock_service

        # Mock the retrieve method with no results (empty list)
        mock_chunks = []
        mock_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_processing_time = 0.080

        mock_service.retrieve = AsyncMock(return_value=(mock_chunks, mock_embedding, mock_processing_time))
        mock_service.convert_internal_chunks_to_api_response = MagicMock(return_value=[])

        # Make request with a query that should not match any content
        response = client.post(
            "/retrieval/search",
            json={
                "query": "completely unrelated query about topics not in the database",
                "top_k": 5,
                "similarity_threshold": 0.8  # High threshold to ensure no matches
            }
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        # Check that we got an empty results list
        assert len(data["results"]) == 0
        assert data["total_results"] == 0

        # Check that other fields are still properly populated
        assert data["query"] == "completely unrelated query about topics not in the database"
        assert data["processing_time"] >= 0
        assert data["request_id"] is not None
        assert data["status"] == "success"