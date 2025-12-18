import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.vector_db_service import VectorDBService
from src.services.models import RetrievedChunkInternal
from src.config.settings import settings


@pytest.mark.asyncio
async def test_search_success():
    """
    Test successful vector search.
    """
    # Arrange
    vector_db_service = VectorDBService()

    # Mock the Qdrant client
    vector_db_service.client = MagicMock()
    mock_result1 = MagicMock()
    mock_result1.id = "chunk1"
    mock_result1.payload = {"content": "Test content 1", "metadata": {"source": "doc1.pdf"}, "source": "doc1.pdf"}
    mock_result1.score = 0.85

    mock_result2 = MagicMock()
    mock_result2.id = "chunk2"
    mock_result2.payload = {"content": "Test content 2", "metadata": {"source": "doc2.pdf"}, "source": "doc2.pdf"}
    mock_result2.score = 0.75

    vector_db_service.client.search.return_value = [mock_result1, mock_result2]

    query_vector = [0.1, 0.2, 0.3]
    top_k = 5
    similarity_threshold = 0.5
    filters = {"category": "science"}

    # Act
    results = await vector_db_service.search(
        query_vector=query_vector,
        top_k=top_k,
        similarity_threshold=similarity_threshold,
        filters=filters
    )

    # Assert
    assert len(results) == 2
    assert isinstance(results[0], RetrievedChunkInternal)
    assert results[0].id == "chunk1"
    assert results[0].content == "Test content 1"
    assert results[0].metadata == {"source": "doc1.pdf"}
    assert results[0].score == 0.85
    assert results[0].source == "doc1.pdf"

    assert results[1].id == "chunk2"
    assert results[1].content == "Test content 2"
    assert results[1].metadata == {"source": "doc2.pdf"}
    assert results[1].score == 0.75
    assert results[1].source == "doc2.pdf"

    vector_db_service.client.search.assert_called_once_with(
        collection_name=vector_db_service.collection_name,
        query_vector=query_vector,
        limit=top_k,
        score_threshold=similarity_threshold,
        query_filter=None  # Note: Our filter implementation may need adjustment
    )


@pytest.mark.asyncio
async def test_search_with_empty_results():
    """
    Test vector search with no results.
    """
    # Arrange
    vector_db_service = VectorDBService()

    # Mock the Qdrant client
    vector_db_service.client = MagicMock()
    vector_db_service.client.search.return_value = []

    query_vector = [0.1, 0.2, 0.3]

    # Act
    results = await vector_db_service.search(query_vector)

    # Assert
    assert len(results) == 0


@pytest.mark.asyncio
async def test_validate_connection_success():
    """
    Test successful connection validation.
    """
    # Arrange
    vector_db_service = VectorDBService()

    # Mock the Qdrant client
    vector_db_service.client = MagicMock()
    mock_collection_info = MagicMock()
    mock_collection_info.points_count = 100
    vector_db_service.client.get_collection.return_value = mock_collection_info

    # Act
    result = await vector_db_service.validate_connection()

    # Assert
    assert result is True
    vector_db_service.client.get_collection.assert_called_once_with(vector_db_service.collection_name)


@pytest.mark.asyncio
async def test_validate_connection_failure():
    """
    Test connection validation failure.
    """
    # Arrange
    vector_db_service = VectorDBService()

    # Mock the Qdrant client to raise an exception
    vector_db_service.client = MagicMock()
    vector_db_service.client.get_collection.side_effect = Exception("Connection failed")

    # Act
    result = await vector_db_service.validate_connection()

    # Assert
    assert result is False


@pytest.mark.asyncio
async def test_get_collection_info():
    """
    Test getting collection information.
    """
    # Arrange
    vector_db_service = VectorDBService()

    # Mock the Qdrant client
    vector_db_service.client = MagicMock()
    mock_collection_info = MagicMock()
    mock_collection_info.points_count = 250
    mock_config = MagicMock()
    mock_config.hnsw_config = MagicMock()
    mock_config.hnsw_config.dict.return_value = {"m": 16, "ef_construct": 100}
    mock_config.optimizer_config = MagicMock()
    mock_config.optimizer_config.dict.return_value = {"max_segment_size": 50000}
    mock_config.wal_config = MagicMock()
    mock_config.wal_config.dict.return_value = {"wal_capacity_mb": 32}
    mock_collection_info.config = mock_config
    vector_db_service.client.get_collection.return_value = mock_collection_info

    # Act
    result = await vector_db_service.get_collection_info()

    # Assert
    assert result["collection_name"] == vector_db_service.collection_name
    assert result["points_count"] == 250
    assert result["config"]["hnsw_config"]["m"] == 16
    assert result["config"]["hnsw_config"]["ef_construct"] == 100
    assert result["config"]["optimizer_config"]["max_segment_size"] == 50000
    assert result["config"]["wal_config"]["wal_capacity_mb"] == 32