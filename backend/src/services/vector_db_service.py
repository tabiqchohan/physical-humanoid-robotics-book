from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from ..config.settings import settings
from ..services.models import RetrievedChunkInternal, VectorSearchResult
from ..services.logger_service import setup_logger
from ..config.constants import QDRANT_DEFAULT_COLLECTION, QDRANT_DISTANCE_METRIC


class VectorDBService:
    """
    Service for interacting with the vector database (Qdrant) for similarity search operations.
    """
    def __init__(self):
        # Initialize Qdrant client based on settings
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key
            )
        else:
            self.client = QdrantClient(
                url=settings.qdrant_url
            )

        self.collection_name = settings.qdrant_collection_name
        self.logger = setup_logger(__name__)

    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[RetrievedChunkInternal]:
        """
        Perform similarity search in the vector database.

        Args:
            query_vector: The embedding vector to search for
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score for results
            filters: Additional filters for the search

        Returns:
            List of RetrievedChunkInternal objects
        """
        try:
            # Validate inputs
            if not query_vector or len(query_vector) == 0:
                raise ValueError("Query vector cannot be empty")

            if top_k <= 0:
                raise ValueError("top_k must be greater than 0")

            if not (0.0 <= similarity_threshold <= 1.0):
                raise ValueError("similarity_threshold must be between 0.0 and 1.0")

            # Build filters if provided
            search_filter = None
            if filters:
                must_conditions = []
                for key, value in filters.items():
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )
                if must_conditions:
                    search_filter = models.Filter(must=must_conditions)

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=similarity_threshold,
                query_filter=search_filter
            )

            # Convert results to RetrievedChunkInternal objects
            retrieved_chunks = []
            for result in results:
                chunk = RetrievedChunkInternal(
                    id=str(result.id),
                    content=result.payload.get('content', '') if result.payload else '',
                    metadata=result.payload.get('metadata', {}) if result.payload else {},
                    score=result.score if result.score else 0.0,
                    source=result.payload.get('source') if result.payload else None
                )
                retrieved_chunks.append(chunk)

            self.logger.info(
                "Vector search completed",
                extra={
                    "collection": self.collection_name,
                    "num_results": len(retrieved_chunks),
                    "top_k": top_k,
                    "similarity_threshold": similarity_threshold
                }
            )

            return retrieved_chunks

        except Exception as e:
            self.logger.error(
                "Failed to perform vector search",
                extra={
                    "error": str(e),
                    "collection": self.collection_name,
                    "top_k": top_k
                }
            )
            raise

    async def validate_connection(self) -> bool:
        """
        Validate that the connection to the vector database is working.

        Returns:
            True if the connection is valid, False otherwise
        """
        try:
            # Try to get collection info to verify connection
            collection_info = self.client.get_collection(self.collection_name)
            self.logger.info(
                "Vector database connection validated",
                extra={
                    "collection": self.collection_name,
                    "points_count": collection_info.points_count
                }
            )
            return True
        except Exception as e:
            self.logger.error(
                "Vector database connection validation failed",
                extra={
                    "error": str(e),
                    "collection": self.collection_name
                }
            )
            return False

    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the vector database collection.

        Returns:
            Dictionary with collection information
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)

            info = {
                "collection_name": self.collection_name,
                "points_count": collection_info.points_count,
                "config": {
                    "hnsw_config": collection_info.config.hnsw_config.dict() if collection_info.config.hnsw_config else None,
                    "optimizer_config": collection_info.config.optimizer_config.dict() if collection_info.config.optimizer_config else None,
                    "wal_config": collection_info.config.wal_config.dict() if collection_info.config.wal_config else None
                }
            }

            return info
        except Exception as e:
            self.logger.error(
                "Failed to get collection info",
                extra={
                    "error": str(e),
                    "collection": self.collection_name
                }
            )
            raise