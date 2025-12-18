from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Optional
import time
import uuid
from ...services.retrieval_service import RetrievalService
from ...api.models.request import SearchRequest, ValidateRequest
from ...api.models.response import SearchResponse, ValidateResponse, ErrorResponse
from ...services.logger_service import setup_logger, set_correlation_id, get_correlation_id
from ...utils.helpers import generate_request_id, calculate_processing_time
from ...services.logger_service import log_api_request, log_retrieval_request
from ...config.constants import PROCESSING_STATUS_SUCCESS, PROCESSING_STATUS_ERROR


router = APIRouter()
logger = setup_logger(__name__)


def get_retrieval_service() -> RetrievalService:
    """
    Dependency to get the retrieval service instance.
    """
    return RetrievalService()


@router.post("/retrieval/search", response_model=SearchResponse)
async def search_endpoint(
    request: SearchRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    """
    Search endpoint to retrieve relevant document chunks from the vector database.
    """
    start_time = time.time()

    # Generate request ID if not provided
    request_id = request.request_id or generate_request_id()

    # Set correlation ID for this request
    set_correlation_id(request_id)

    try:
        # Perform the retrieval
        retrieved_chunks, query_embedding, processing_time = await retrieval_service.retrieve(
            query=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
            filters=request.filters
        )

        # Convert internal chunks to API response format
        api_chunks = retrieval_service.convert_internal_chunks_to_api_response(retrieved_chunks)

        # Create the response
        response = SearchResponse(
            query=request.query,
            results=api_chunks,
            total_results=len(api_chunks),
            processing_time=processing_time,
            query_embedding=query_embedding if request.top_k <= 10 else None,  # Only include embedding for smaller result sets
            request_id=request_id,
            status=PROCESSING_STATUS_SUCCESS
        )

        # Calculate total processing time including response preparation
        total_processing_time = calculate_processing_time(start_time)

        # Log the retrieval request
        log_retrieval_request(
            logger=logger,
            request_id=request_id,
            query=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
            num_results=len(api_chunks),
            processing_time=total_processing_time
        )

        # Log the API request
        log_api_request(
            logger=logger,
            request_id=request_id,
            endpoint="/retrieval/search",
            method="POST",
            processing_time=total_processing_time,
            status_code=200
        )

        return response

    except ValueError as e:
        # Handle validation errors
        error_response = ErrorResponse(
            error=str(e),
            type="validation_error",
            details={"field": "query", "reason": str(e)},
            request_id=request_id
        )

        processing_time = calculate_processing_time(start_time)

        logger.error(
            "Search request validation failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "processing_time": processing_time
            }
        )

        log_api_request(
            logger=logger,
            request_id=request_id,
            endpoint="/retrieval/search",
            method="POST",
            processing_time=processing_time,
            status_code=400
        )

        raise HTTPException(status_code=400, detail=error_response)

    except Exception as e:
        # Handle other errors
        error_response = ErrorResponse(
            error=f"Internal server error: {str(e)}",
            type="internal_error",
            details={},
            request_id=request_id
        )

        processing_time = calculate_processing_time(start_time)

        logger.error(
            "Search request failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "processing_time": processing_time
            }
        )

        log_api_request(
            logger=logger,
            request_id=request_id,
            endpoint="/retrieval/search",
            method="POST",
            processing_time=processing_time,
            status_code=500
        )

        raise HTTPException(status_code=500, detail=error_response)


@router.post("/retrieval/validate", response_model=ValidateResponse)
async def validate_endpoint(
    request: ValidateRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    """
    Validate endpoint to check if a query can be processed.
    """
    start_time = time.time()

    # Generate request ID if not provided
    request_id = request.request_id or generate_request_id()

    # Set correlation ID for this request
    set_correlation_id(request_id)

    try:
        # Validate the query
        validation_result = await retrieval_service.validate_query(request.query)

        # Create the response
        response = ValidateResponse(
            request_id=request_id,
            is_valid=validation_result["is_valid"],
            message=validation_result["message"],
            suggestions=validation_result["suggestions"]
        )

        processing_time = calculate_processing_time(start_time)

        logger.info(
            "Query validation completed",
            extra={
                "request_id": request_id,
                "is_valid": validation_result["is_valid"],
                "processing_time": processing_time
            }
        )

        log_api_request(
            logger=logger,
            request_id=request_id,
            endpoint="/retrieval/validate",
            method="POST",
            processing_time=processing_time,
            status_code=200
        )

        return response

    except Exception as e:
        error_response = ErrorResponse(
            error=f"Validation failed: {str(e)}",
            type="internal_error",
            details={},
            request_id=request_id
        )

        processing_time = calculate_processing_time(start_time)

        logger.error(
            "Query validation failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "processing_time": processing_time
            }
        )

        log_api_request(
            logger=logger,
            request_id=request_id,
            endpoint="/retrieval/validate",
            method="POST",
            processing_time=processing_time,
            status_code=500
        )

        raise HTTPException(status_code=500, detail=error_response)