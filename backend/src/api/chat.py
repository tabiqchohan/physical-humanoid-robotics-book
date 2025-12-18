from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from typing import List
import uuid
from datetime import datetime
import logging

from src.models.query import QueryRequest, QueryResponse
from src.services.rag import RAGService
from src.config.settings import settings

# Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize RAG service
rag_service = RAGService()


@router.post("/chat/query", response_model=QueryResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def query_full_book_content(request: Request, query_request: QueryRequest):
    """
    Submit a query to the RAG system to search across full book content
    """
    try:
        logger.info(f"Processing query: {query_request.query[:50]}...")

        # Generate session ID if not provided
        session_id = query_request.sessionId or str(uuid.uuid4())

        # Process the query using RAG service
        response_text, sources = await rag_service.query(
            query_text=query_request.query,
            context=query_request.context
        )

        # Create response
        response = QueryResponse(
            response=response_text,
            sources=sources,
            sessionId=session_id,
            timestamp=datetime.now().isoformat()
        )

        logger.info(f"Query processed successfully, session: {session_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/chat/query-selected-text", response_model=QueryResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def query_selected_text_content(request: Request, query_request: QueryRequest):
    """
    Submit a query specifically about selected text
    """
    try:
        if not query_request.context:
            raise HTTPException(status_code=400, detail="Context (selected text) is required for this endpoint")

        logger.info(f"Processing selected text query: {query_request.query[:50]}...")

        # Generate session ID if not provided
        session_id = query_request.sessionId or str(uuid.uuid4())

        # Process the query using RAG service with selected text context
        response_text, sources = await rag_service.query(
            query_text=query_request.query,
            context=query_request.context
        )

        # Create response
        response = QueryResponse(
            response=response_text,
            sources=sources,
            sessionId=session_id,
            timestamp=datetime.now().isoformat()
        )

        logger.info(f"Selected text query processed successfully, session: {session_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing selected text query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")