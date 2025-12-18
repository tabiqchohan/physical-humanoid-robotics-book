from typing import List, Optional, Dict, Any
import time
from ..config.settings import settings
from ..services.models import QueryRequestInternal, RetrievedChunkInternal
from ..services.embedding_service import EmbeddingService
from ..services.vector_db_service import VectorDBService
from ..services.logger_service import setup_logger
from ..api.models.response import RetrievedChunk


class RetrievalService:
    """
    Service for orchestrating the retrieval process: embedding generation and vector search.
    """
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_db_service = VectorDBService()
        self.logger = setup_logger(__name__)

    async def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ):
        """
        Perform the full retrieval process: generate embedding and search vector database.

        Args:
            query: The natural language query to process
            top_k: Number of results to return (uses default if not provided)
            similarity_threshold: Minimum similarity score for results (uses default if not provided)
            filters: Additional filters for the search

        Returns:
            Tuple of (retrieved_chunks, query_embedding, processing_time)
        """
        start_time = time.time()

        try:
            # Set defaults if not provided
            top_k = top_k or settings.default_top_k
            similarity_threshold = similarity_threshold or settings.default_similarity_threshold

            # Validate the query
            query_request = QueryRequestInternal(
                query=query,
                top_k=top_k,
                similarity_threshold=similarity_threshold,
                filters=filters
            )
            query_request.validate_query()

            # Generate embedding for the query
            embedding_result = await self.embedding_service.generate_embedding(query)

            # Search in the vector database
            retrieved_chunks = await self.vector_db_service.search(
                query_vector=embedding_result.embedding,
                top_k=top_k,
                similarity_threshold=similarity_threshold,
                filters=filters
            )

            processing_time = time.time() - start_time

            self.logger.info(
                "Retrieval completed successfully",
                extra={
                    "query_length": len(query),
                    "num_results": len(retrieved_chunks),
                    "top_k": top_k,
                    "similarity_threshold": similarity_threshold,
                    "processing_time": processing_time
                }
            )

            return retrieved_chunks, embedding_result.embedding, processing_time

        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(
                "Retrieval failed",
                extra={
                    "error": str(e),
                    "query_length": len(query) if 'query' in locals() else 0,
                    "top_k": top_k,
                    "processing_time": processing_time
                }
            )
            raise

    async def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate that a query is properly formatted and can be processed.

        Args:
            query: The query to validate

        Returns:
            Dictionary with validation results
        """
        try:
            # Basic validation
            if not query or len(query.strip()) == 0:
                return {
                    "is_valid": False,
                    "message": "Query cannot be empty",
                    "suggestions": ["Provide a non-empty query"]
                }

            if len(query) > settings.max_query_length:
                return {
                    "is_valid": False,
                    "message": f"Query exceeds maximum length of {settings.max_query_length} characters",
                    "suggestions": [f"Shorten query to {settings.max_query_length} characters or less"]
                }

            # Test embedding generation
            try:
                await self.embedding_service.generate_embedding(query)
            except Exception as e:
                return {
                    "is_valid": False,
                    "message": f"Query cannot be embedded: {str(e)}",
                    "suggestions": ["Check that the query is in a supported language"]
                }

            return {
                "is_valid": True,
                "message": "Query is valid and can be processed",
                "suggestions": None
            }

        except Exception as e:
            self.logger.error(
                "Query validation failed",
                extra={
                    "error": str(e),
                    "query_length": len(query) if query else 0
                }
            )
            return {
                "is_valid": False,
                "message": f"Validation error: {str(e)}",
                "suggestions": None
            }

    def convert_internal_chunks_to_api_response(self, internal_chunks: List[RetrievedChunkInternal]) -> List[RetrievedChunk]:
        """
        Convert internal RetrievedChunkInternal objects to API-compatible RetrievedChunk objects.

        Args:
            internal_chunks: List of internal chunk objects

        Returns:
            List of API-compatible chunk objects
        """
        api_chunks = []
        for internal_chunk in internal_chunks:
            api_chunk = RetrievedChunk(
                id=internal_chunk.id,
                content=internal_chunk.content,
                metadata=internal_chunk.metadata,
                score=internal_chunk.score,
                source=internal_chunk.source
            )
            api_chunks.append(api_chunk)

        return api_chunks