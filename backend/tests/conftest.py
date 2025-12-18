import pytest
import os
from unittest.mock import Mock, patch


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    """
    Override settings for tests.
    """
    # Set test-specific environment variables
    os.environ["ENVIRONMENT"] = "test"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["COHERE_API_KEY"] = "test-cohere-api-key"
    os.environ["QDRANT_URL"] = "http://localhost:6333"
    os.environ["QDRANT_COLLECTION_NAME"] = "test_documents"
    os.environ["DEFAULT_TOP_K"] = "5"
    os.environ["DEFAULT_SIMILARITY_THRESHOLD"] = "0.5"
    os.environ["MAX_QUERY_LENGTH"] = "1000"

    # Import settings after environment variables are set
    from src.config.settings import settings
    yield settings


@pytest.fixture
def mock_embedding_service():
    """
    Mock embedding service for testing.
    """
    with patch('src.services.embedding_service.EmbeddingService') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_vector_db_service():
    """
    Mock vector database service for testing.
    """
    with patch('src.services.vector_db_service.VectorDBService') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def sample_retrieved_chunk():
    """
    Sample retrieved chunk for testing.
    """
    from src.services.models import RetrievedChunkInternal
    return RetrievedChunkInternal(
        id="test_chunk_1",
        content="This is a test chunk of content for retrieval testing.",
        metadata={"source": "test_document.pdf", "page": 1},
        score=0.85,
        source="test_document.pdf"
    )


@pytest.fixture
def sample_search_request():
    """
    Sample search request for testing.
    """
    from src.api.models.request import SearchRequest
    return SearchRequest(
        query="What are the benefits of renewable energy?",
        top_k=3,
        similarity_threshold=0.5
    )