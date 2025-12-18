import pytest
from unittest.mock import Mock, patch
from src.services.retrieval_service import RetrievalService
from src.models.document_chunk import DocumentChunk
from src.models.retrieval_result import RetrievalResult


class TestRetrievalServiceMetadata:
    """
    Unit tests for metadata validation in RetrievalService
    """

    @pytest.fixture
    def retrieval_service(self):
        with patch('src.services.retrieval_service.EmbeddingService') as mock_embedding, \
             patch('src.services.retrieval_service.QdrantService') as mock_qdrant:
            service = RetrievalService()
            service.embedding_service = mock_embedding
            service.qdrant_service = mock_qdrant
            return service

    def test_validate_metadata_completeness_all_complete(self, retrieval_service):
        """
        Test that validate_metadata_completeness correctly identifies complete metadata
        """
        # Create retrieval results with complete metadata
        chunk1 = DocumentChunk(
            chunk_id="chunk-001",
            content="Test content 1",
            url="http://example.com/1",
            title="Test Title 1",
            section="Section 1"
        )
        result1 = RetrievalResult(
            chunk=chunk1,
            similarity_score=0.9,
            rank=1
        )

        chunk2 = DocumentChunk(
            chunk_id="chunk-002",
            content="Test content 2",
            url="http://example.com/2",
            title="Test Title 2",
            section="Section 2"
        )
        result2 = RetrievalResult(
            chunk=chunk2,
            similarity_score=0.8,
            rank=2
        )

        results = [result1, result2]

        validation_result = retrieval_service.validate_metadata_completeness(results)

        assert validation_result["total_chunks"] == 2
        assert validation_result["chunks_with_complete_metadata"] == 2
        assert validation_result["chunks_with_missing_metadata"] == 0
        assert validation_result["metadata_completion_percentage"] == 100.0
        assert len(validation_result["missing_fields_per_chunk"]) == 0
        assert all(detail["status"] == "complete" for detail in validation_result["validation_details"])

    def test_validate_metadata_completeness_missing_fields(self, retrieval_service):
        """
        Test that validate_metadata_completeness correctly identifies missing metadata fields
        """
        # Create retrieval results with some missing metadata
        chunk1 = DocumentChunk(
            chunk_id="",  # Missing chunk_id
            content="Test content 1",
            url="http://example.com/1",
            title="Test Title 1",
            section="Section 1"
        )
        result1 = RetrievalResult(
            chunk=chunk1,
            similarity_score=0.9,
            rank=1
        )

        chunk2 = DocumentChunk(
            chunk_id="chunk-002",
            content="",  # Missing content
            url="",  # Missing url
            title="Test Title 2",
            section="Section 2"
        )
        result2 = RetrievalResult(
            chunk=chunk2,
            similarity_score=0.8,
            rank=2
        )

        chunk3 = DocumentChunk(
            chunk_id="chunk-003",
            content="Test content 3",
            url="http://example.com/3",
            title="Test Title 3",
            section="Section 3"
        )
        result3 = RetrievalResult(
            chunk=chunk3,
            similarity_score=0.7,
            rank=3
        )

        results = [result1, result2, result3]

        validation_result = retrieval_service.validate_metadata_completeness(results)

        assert validation_result["total_chunks"] == 3
        assert validation_result["chunks_with_complete_metadata"] == 1
        assert validation_result["chunks_with_missing_metadata"] == 2
        assert abs(validation_result["metadata_completion_percentage"] - 33.33) < 0.01  # 1/3

        # Check missing fields for first chunk
        missing_chunk1 = next(
            item for item in validation_result["missing_fields_per_chunk"]
            if item["chunk_id"] == ""
        )
        assert "chunk_id" in missing_chunk1["missing_fields"]

        # Check missing fields for second chunk
        missing_chunk2 = next(
            item for item in validation_result["missing_fields_per_chunk"]
            if item["chunk_id"] == "chunk-002"
        )
        assert "url" in missing_chunk2["missing_fields"]
        assert "content" in missing_chunk2["missing_fields"]

    def test_validate_metadata_completeness_empty_results(self, retrieval_service):
        """
        Test that validate_metadata_completeness handles empty results correctly
        """
        validation_result = retrieval_service.validate_metadata_completeness([])

        assert validation_result["total_chunks"] == 0
        assert validation_result["chunks_with_complete_metadata"] == 0
        assert validation_result["chunks_with_missing_metadata"] == 0
        assert validation_result["metadata_completion_percentage"] == 0.0
        assert len(validation_result["missing_fields_per_chunk"]) == 0
        assert len(validation_result["validation_details"]) == 0

    def test_validate_similarity_score_interpretability_valid_range(self, retrieval_service):
        """
        Test that validate_similarity_score_interpretability correctly validates score range
        """
        # Create results with valid similarity scores
        chunk1 = DocumentChunk(
            chunk_id="chunk-001",
            content="Test content 1",
            url="http://example.com/1",
            title="Test Title 1",
            section="Section 1"
        )
        result1 = RetrievalResult(
            chunk=chunk1,
            similarity_score=0.9,
            rank=1
        )

        chunk2 = DocumentChunk(
            chunk_id="chunk-002",
            content="Test content 2",
            url="http://example.com/2",
            title="Test Title 2",
            section="Section 2"
        )
        result2 = RetrievalResult(
            chunk=chunk2,
            similarity_score=0.7,
            rank=2
        )

        chunk3 = DocumentChunk(
            chunk_id="chunk-003",
            content="Test content 3",
            url="http://example.com/3",
            title="Test Title 3",
            section="Section 3"
        )
        result3 = RetrievalResult(
            chunk=chunk3,
            similarity_score=0.5,
            rank=3
        )

        results = [result1, result2, result3]

        validation_result = retrieval_service.validate_similarity_score_interpretability(results)

        assert validation_result["is_valid"] is True
        assert validation_result["message"] == "Similarity scores are interpretable"
        assert validation_result["score_range"]["min"] == 0.5
        assert validation_result["score_range"]["max"] == 0.9
        assert abs(validation_result["score_range"]["avg"] - 0.7) < 0.001  # (0.9 + 0.7 + 0.5) / 3 ≈ 0.7
        assert validation_result["monotonic_ranking"] is True  # Scores decrease with rank

    def test_validate_similarity_score_interpretability_invalid_range(self, retrieval_service):
        """
        Test that validate_similarity_score_interpretability detects invalid scores
        """
        # Instead of creating invalid RetrievalResult objects, we'll test the function directly
        # with a mock that has invalid scores to simulate the scenario
        from unittest.mock import Mock

        # Create mock results with invalid similarity scores
        mock_result1 = Mock()
        mock_result1.similarity_score = 1.5  # Invalid: > 1.0
        mock_result1.rank = 1

        mock_result2 = Mock()
        mock_result2.similarity_score = 0.7
        mock_result2.rank = 2

        results = [mock_result1, mock_result2]

        validation_result = retrieval_service.validate_similarity_score_interpretability(results)

        assert validation_result["is_valid"] is False
        assert "Some similarity scores are out of range [0, 1]" in validation_result["message"]
        assert validation_result["score_range"]["min"] == 0.7
        assert validation_result["score_range"]["max"] == 1.5
        assert validation_result["score_range"]["avg"] == 1.1  # (1.5 + 0.7) / 2

    def test_validate_similarity_score_interpretability_empty_results(self, retrieval_service):
        """
        Test that validate_similarity_score_interpretability handles empty results correctly
        """
        validation_result = retrieval_service.validate_similarity_score_interpretability([])

        assert validation_result["is_valid"] is True
        assert validation_result["message"] == "No results to validate"
        assert validation_result["score_range"]["min"] is None
        assert validation_result["score_range"]["max"] is None
        assert validation_result["score_range"]["avg"] is None
        assert validation_result["monotonic_ranking"] is True