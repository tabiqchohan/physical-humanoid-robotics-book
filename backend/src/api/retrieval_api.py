from fastapi import FastAPI, HTTPException, Request
from typing import Dict, Any
from src.models.retrieval_request import RetrievalRequest
from src.models.retrieval_response import RetrievalResponse
from src.models.validation_test import ValidationTest
from src.models.validation_result import ValidationResult
from src.services.retrieval_service import RetrievalService
from src.services.validation_service import ValidationService
from src.config.settings import settings
import time
import logging

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="RAG Retrieval Validation API"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

retrieval_service = RetrievalService()
validation_service = ValidationService()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {(time.time() - start):.3f}s"
    )
    return response


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "dependencies": {"cohere": "not_checked", "qdrant": "not_checked"},
    }


@app.post("/retrieval/search", response_model=RetrievalResponse)
async def search_endpoint(request: RetrievalRequest):
    try:
        results, _, total_chunks, exec_time = retrieval_service.retrieve(
            query_text=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
            filters=request.filters,
        )

        # ✅ Convert service objects → API-safe dicts
        formatted_results = [
            {
                "chunk": {
                    "chunk_id": r.chunk.chunk_id,
                    "content": r.chunk.content,
                    "url": r.chunk.url,
                    "title": r.chunk.title,
                    "section": r.chunk.section,
                },
                "similarity_score": r.similarity_score,
                "rank": r.rank,
            }
            for r in results
        ]

        return {
            "query": request.query,
            "results": formatted_results,
            "total_chunks_searched": total_chunks,
            "execution_time_ms": exec_time,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/retrieval/validate", response_model=ValidationResult)
async def validate_endpoint(validation_test: ValidationTest):
    try:
        return validation_service.run_validation_test(validation_test)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
