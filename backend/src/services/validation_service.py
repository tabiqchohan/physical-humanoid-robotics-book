from typing import Dict, Any, List
from src.services.retrieval_service import RetrievalService
from src.models.validation_test import ValidationTest
from src.models.validation_result import ValidationResult
from src.models.retrieval_result import RetrievalResult
import logging

logger = logging.getLogger(__name__)


class ValidationService:
    """
    Service class for validating the retrieval pipeline
    """

    def __init__(self):
        self.retrieval_service = RetrievalService()

    def run_validation_test(self, validation_test: ValidationTest) -> ValidationResult:
        """
        Run a validation test and return the results
        """
        try:
            # Perform retrieval with the test query
            results, query_embedding, total_chunks_searched, execution_time = self.retrieval_service.retrieve(
                query_text=validation_test.query,
                top_k=validation_test.top_k,
                similarity_threshold=validation_test.similarity_threshold,
                filters=validation_test.metadata_filters
            )

            # Calculate validation metrics
            retrieved_chunk_ids = [result.chunk.chunk_id for result in results]
            expected_chunk_ids = validation_test.expected_chunks

            relevant_retrieved = len(set(retrieved_chunk_ids) & set(expected_chunk_ids))
            total_retrieved = len(retrieved_chunk_ids)
            total_relevant = len(expected_chunk_ids)

            precision = relevant_retrieved / total_retrieved if total_retrieved > 0 else 0
            recall = relevant_retrieved / total_relevant if total_relevant > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            # Calculate accuracy score (simple average of precision and recall for this implementation)
            accuracy_score = (precision + recall) / 2 if total_retrieved > 0 or total_relevant > 0 else 0

            # Determine if test passes (using configurable threshold, defaulting to 0.7)
            pass_validation = accuracy_score >= 0.7

            # Create validation result
            validation_result = ValidationResult(
                test_id=validation_test.test_id,
                query=validation_test.query,
                retrieved_results=results,
                accuracy_score=accuracy_score,
                pass_validation=pass_validation,
                details={
                    "retrieved_chunk_ids": retrieved_chunk_ids,
                    "expected_chunk_ids": expected_chunk_ids,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1_score,
                    "execution_time_ms": execution_time
                }
            )

            return validation_result

        except Exception as e:
            logger.error(f"Error running validation test: {str(e)}")
            raise

    def validate_retrieval_accuracy(self, query: str, expected_chunks: List[str], top_k: int = 5) -> Dict[str, Any]:
        """
        Validate retrieval accuracy for a specific query against expected chunks
        """
        try:
            # Perform retrieval
            results, _, _, _ = self.retrieval_service.retrieve(query_text=query, top_k=top_k)

            # Extract retrieved chunk IDs
            retrieved_chunk_ids = [result.chunk.chunk_id for result in results]

            # Calculate metrics
            relevant_retrieved = len(set(retrieved_chunk_ids) & set(expected_chunks))
            total_retrieved = len(retrieved_chunk_ids)
            total_relevant = len(expected_chunks)

            precision = relevant_retrieved / total_retrieved if total_retrieved > 0 else 0
            recall = relevant_retrieved / total_relevant if total_relevant > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            accuracy_score = (precision + recall) / 2 if total_retrieved > 0 or total_relevant > 0 else 0

            return {
                "query": query,
                "accuracy_score": accuracy_score,
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "retrieved_chunks": retrieved_chunk_ids,
                "expected_chunks": expected_chunks,
                "relevant_retrieved": relevant_retrieved
            }
        except Exception as e:
            logger.error(f"Error validating retrieval accuracy: {str(e)}")
            raise

    def validate_metadata_completeness_for_test(self, results: List[RetrievalResult]) -> Dict[str, Any]:
        """
        Validate metadata completeness specifically for validation purposes
        """
        return self.retrieval_service.validate_metadata_completeness(results)

    def validate_similarity_score_interpretability_for_test(self, results: List[RetrievalResult]) -> Dict[str, Any]:
        """
        Validate similarity score interpretability specifically for validation purposes
        """
        return self.retrieval_service.validate_similarity_score_interpretability(results)