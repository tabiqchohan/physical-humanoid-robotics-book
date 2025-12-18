import cohere
from typing import List, Optional
from ..config.settings import settings
from ..config.constants import COHERE_EMBED_MODEL, COHERE_EMBED_INPUT_TYPE
from ..services.models import EmbeddingResult
from ..services.logger_service import setup_logger
from ..utils.helpers import is_valid_embedding


class EmbeddingService:
    """
    Service for generating embeddings using the Cohere API.
    """
    def __init__(self):
        self.client = cohere.Client(settings.cohere_api_key)
        self.logger = setup_logger(__name__)

    async def generate_embeddings(self, texts: List[str], model: Optional[str] = None) -> List[EmbeddingResult]:
        """
        Generate embeddings for a list of texts using Cohere.

        Args:
            texts: List of texts to embed
            model: Model to use for embedding (uses default if not provided)

        Returns:
            List of EmbeddingResult objects
        """
        model = model or settings.cohere_model

        try:
            # Generate embeddings using Cohere
            response = self.client.embed(
                texts=texts,
                model=model or COHERE_EMBED_MODEL,
                input_type=COHERE_EMBED_INPUT_TYPE
            )

            # Validate the response
            if not response.embeddings or len(response.embeddings) != len(texts):
                raise ValueError(f"Expected {len(texts)} embeddings, got {len(response.embeddings) if response.embeddings else 0}")

            results = []
            for i, embedding_vector in enumerate(response.embeddings):
                if not is_valid_embedding(embedding_vector):
                    raise ValueError(f"Invalid embedding at index {i}")

                result = EmbeddingResult(
                    text=texts[i],
                    embedding=embedding_vector,
                    model=model or COHERE_EMBED_MODEL
                )
                results.append(result)

            self.logger.info(
                "Successfully generated embeddings",
                extra={
                    "num_texts": len(texts),
                    "model": model,
                    "num_results": len(results)
                }
            )

            return results

        except Exception as e:
            self.logger.error(
                "Failed to generate embeddings",
                extra={
                    "error": str(e),
                    "num_texts": len(texts),
                    "model": model
                }
            )
            raise

    async def generate_embedding(self, text: str, model: Optional[str] = None) -> EmbeddingResult:
        """
        Generate a single embedding for a text.

        Args:
            text: Text to embed
            model: Model to use for embedding (uses default if not provided)

        Returns:
            EmbeddingResult object
        """
        results = await self.generate_embeddings([text], model)
        return results[0]

    async def validate_embedding_model(self, model: str) -> bool:
        """
        Validate that the specified embedding model is available.

        Args:
            model: Model name to validate

        Returns:
            True if the model is available, False otherwise
        """
        try:
            # Test the model with a short text
            test_text = "test"
            response = self.client.embed(
                texts=[test_text],
                model=model,
                input_type=COHERE_EMBED_INPUT_TYPE
            )
            return len(response.embeddings) > 0 if response.embeddings else False
        except Exception:
            return False