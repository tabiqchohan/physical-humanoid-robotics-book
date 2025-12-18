import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.embedding_service import EmbeddingService
from src.services.models import EmbeddingResult
from src.config.constants import COHERE_EMBED_MODEL, COHERE_EMBED_INPUT_TYPE


@pytest.mark.asyncio
async def test_generate_embeddings():
    """
    Test successful generation of embeddings for multiple texts.
    """
    # Arrange
    embedding_service = EmbeddingService()

    # Mock the Cohere client
    embedding_service.client = MagicMock()
    mock_response = MagicMock()
    mock_response.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    embedding_service.client.embed.return_value = mock_response

    texts = ["text1", "text2"]

    # Act
    results = await embedding_service.generate_embeddings(texts)

    # Assert
    assert len(results) == 2
    assert isinstance(results[0], EmbeddingResult)
    assert results[0].text == "text1"
    assert results[0].embedding == [0.1, 0.2, 0.3]
    assert results[0].model == COHERE_EMBED_MODEL

    assert results[1].text == "text2"
    assert results[1].embedding == [0.4, 0.5, 0.6]
    assert results[1].model == COHERE_EMBED_MODEL

    embedding_service.client.embed.assert_called_once_with(
        texts=texts,
        model=COHERE_EMBED_MODEL,
        input_type=COHERE_EMBED_INPUT_TYPE
    )


@pytest.mark.asyncio
async def test_generate_embedding():
    """
    Test successful generation of a single embedding.
    """
    # Arrange
    embedding_service = EmbeddingService()

    # Mock the Cohere client
    embedding_service.client = MagicMock()
    mock_response = MagicMock()
    mock_response.embeddings = [[0.7, 0.8, 0.9]]
    embedding_service.client.embed.return_value = mock_response

    text = "single text"

    # Act
    result = await embedding_service.generate_embedding(text)

    # Assert
    assert isinstance(result, EmbeddingResult)
    assert result.text == "single text"
    assert result.embedding == [0.7, 0.8, 0.9]
    assert result.model == COHERE_EMBED_MODEL

    embedding_service.client.embed.assert_called_once_with(
        texts=[text],
        model=COHERE_EMBED_MODEL,
        input_type=COHERE_EMBED_INPUT_TYPE
    )


@pytest.mark.asyncio
async def test_validate_embedding_model():
    """
    Test validation of embedding model availability.
    """
    # Arrange
    embedding_service = EmbeddingService()

    # Mock the Cohere client
    embedding_service.client = MagicMock()
    mock_response = MagicMock()
    mock_response.embeddings = [[0.1, 0.2, 0.3]]
    embedding_service.client.embed.return_value = mock_response

    # Act
    result = await embedding_service.validate_embedding_model("test-model")

    # Assert
    assert result is True
    embedding_service.client.embed.assert_called_once_with(
        texts=["test"],
        model="test-model",
        input_type=COHERE_EMBED_INPUT_TYPE
    )


@pytest.mark.asyncio
async def test_validate_embedding_model_failure():
    """
    Test validation of embedding model when it fails.
    """
    # Arrange
    embedding_service = EmbeddingService()

    # Mock the Cohere client to raise an exception
    embedding_service.client = MagicMock()
    embedding_service.client.embed.side_effect = Exception("API error")

    # Act
    result = await embedding_service.validate_embedding_model("invalid-model")

    # Assert
    assert result is False


def test_is_valid_embedding():
    """
    Test the is_valid_embedding utility function (imported in the service).
    """
    from src.utils.helpers import is_valid_embedding

    # Valid embedding
    assert is_valid_embedding([0.1, 0.5, 0.9])

    # Invalid embeddings
    assert not is_valid_embedding([])
    assert not is_valid_embedding([1.5, 2.0])  # Values outside [-1, 1] range
    assert not is_valid_embedding("not a list")
    assert not is_valid_embedding([0.1, "not a number", 0.5])