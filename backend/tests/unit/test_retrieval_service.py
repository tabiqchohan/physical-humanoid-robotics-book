import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.retrieval_service import RetrievalService
from src.services.models import RetrievedChunkInternal
from src.api.models.response import RetrievedChunk


@pytest.mark.asyncio
async def test_retrieve_success():
    """
    Test successful retrieval of document chunks.
    """
    # Arrange
    retrieval_service = RetrievalService()

    # Mock the services
    retrieval_service.embedding_service = MagicMock()
    retrieval_service.vector_db_service = MagicMock()

    query = "What are the benefits of renewable energy?"
    expected_embedding = [0.1, 0.2, 0.3]
    expected_chunks = [
        RetrievedChunkInternal(
            id="chunk1",
            content="Renewable energy reduces carbon emissions.",
            metadata={"source": "doc1.pdf"},
            score=0.85,
            source="doc1.pdf"
        )
    ]

    retrieval_service.embedding_service.generate_embedding = AsyncMock(return_value=MagicMock(embedding=expected_embedding))
    retrieval_service.vector_db_service.search = AsyncMock(return_value=expected_chunks)

    # Act
    result_chunks, result_embedding, processing_time = await retrieval_service.retrieve(query)

    # Assert
    assert result_chunks == expected_chunks
    assert result_embedding == expected_embedding
    assert processing_time >= 0
    retrieval_service.embedding_service.generate_embedding.assert_called_once_with(query)
    retrieval_service.vector_db_service.search.assert_called_once_with(
        query_vector=expected_embedding,
        top_k=5,  # default
        similarity_threshold=0.5,  # default
        filters=None
    )


@pytest.mark.asyncio
async def test_retrieve_with_custom_params():
    """
    Test retrieval with custom parameters.
    """
    # Arrange
    retrieval_service = RetrievalService()

    # Mock the services
    retrieval_service.embedding_service = MagicMock()
    retrieval_service.vector_db_service = MagicMock()

    query = "Test query"
    top_k = 10
    similarity_threshold = 0.7
    filters = {"category": "science"}
    expected_embedding = [0.4, 0.5, 0.6]
    expected_chunks = [
        RetrievedChunkInternal(
            id="chunk2",
            content="Test content",
            metadata={"source": "test.pdf"},
            score=0.9,
            source="test.pdf"
        )
    ]

    retrieval_service.embedding_service.generate_embedding = AsyncMock(return_value=MagicMock(embedding=expected_embedding))
    retrieval_service.vector_db_service.search = AsyncMock(return_value=expected_chunks)

    # Act
    result_chunks, result_embedding, _ = await retrieval_service.retrieve(
        query, top_k=top_k, similarity_threshold=similarity_threshold, filters=filters
    )

    # Assert
    assert result_chunks == expected_chunks
    retrieval_service.vector_db_service.search.assert_called_once_with(
        query_vector=expected_embedding,
        top_k=top_k,
        similarity_threshold=similarity_threshold,
        filters=filters
    )


@pytest.mark.asyncio
async def test_validate_query_success():
    """
    Test successful query validation.
    """
    # Arrange
    retrieval_service = RetrievalService()
    retrieval_service.embedding_service = MagicMock()
    retrieval_service.embedding_service.generate_embedding = AsyncMock(return_value=MagicMock())

    # Act
    result = await retrieval_service.validate_query("Valid query text")

    # Assert
    assert result["is_valid"] is True
    assert result["message"] == "Query is valid and can be processed"


@pytest.mark.asyncio
async def test_validate_query_empty():
    """
    Test validation of empty query.
    """
    # Arrange
    retrieval_service = RetrievalService()

    # Act
    result = await retrieval_service.validate_query("")

    # Assert
    assert result["is_valid"] is False
    assert "cannot be empty" in result["message"]


@pytest.mark.asyncio
async def test_validate_query_too_long():
    """
    Test validation of query that exceeds maximum length.
    """
    # Arrange
    retrieval_service = RetrievalService()
    long_query = "x" * 2000  # Assuming this exceeds max length

    # Act
    result = await retrieval_service.validate_query(long_query)

    # Assert
    assert result["is_valid"] is False
    assert "exceeds maximum length" in result["message"]


@pytest.mark.asyncio
async def test_validate_query_embedding_error():
    """
    Test validation when embedding generation fails.
    """
    # Arrange
    retrieval_service = RetrievalService()
    retrieval_service.embedding_service = MagicMock()
    retrieval_service.embedding_service.generate_embedding.side_effect = Exception("Embedding error")

    # Act
    result = await retrieval_service.validate_query("Problematic query")

    # Assert
    assert result["is_valid"] is False
    assert "cannot be embedded" in result["message"]


def test_convert_internal_chunks_to_api_response():
    """
    Test conversion from internal chunk objects to API response objects.
    """
    # Arrange
    retrieval_service = RetrievalService()

    internal_chunks = [
        RetrievedChunkInternal(
            id="chunk1",
            content="Test content 1",
            metadata={"source": "doc1.pdf", "page": 1},
            score=0.85,
            source="doc1.pdf"
        ),
        RetrievedChunkInternal(
            id="chunk2",
            content="Test content 2",
            metadata={"source": "doc2.pdf", "page": 2},
            score=0.75,
            source="doc2.pdf"
        )
    ]

    # Act
    api_chunks = retrieval_service.convert_internal_chunks_to_api_response(internal_chunks)

    # Assert
    assert len(api_chunks) == 2
    assert api_chunks[0].id == "chunk1"
    assert api_chunks[0].content == "Test content 1"
    assert api_chunks[0].metadata == {"source": "doc1.pdf", "page": 1}
    assert api_chunks[0].score == 0.85
    assert api_chunks[0].source == "doc1.pdf"

    assert api_chunks[1].id == "chunk2"
    assert api_chunks[1].content == "Test content 2"
    assert api_chunks[1].metadata == {"source": "doc2.pdf", "page": 2}
    assert api_chunks[1].score == 0.75
    assert api_chunks[1].source == "doc2.pdf"