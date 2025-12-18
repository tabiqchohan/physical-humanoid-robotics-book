"""
Application constants used throughout the RAG Chatbot Backend.
"""

# API Response Constants
DEFAULT_TOP_K = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.5
MAX_QUERY_LENGTH = 1000
MAX_TOP_K = 100

# Cohere Constants
COHERE_EMBED_MODEL = "embed-multilingual-v3.0"
COHERE_EMBED_INPUT_TYPE = "search_query"

# Qdrant Constants
QDRANT_DEFAULT_COLLECTION = "documents"
QDRANT_DISTANCE_METRIC = "Cosine"

# Logging Constants
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
CORRELATION_ID_HEADER = "X-Request-ID"

# Error Types
EMBEDDING_ERROR = "embedding_error"
DATABASE_ERROR = "database_error"
VALIDATION_ERROR = "validation_error"
INTERNAL_ERROR = "internal_error"

# Processing Status
PROCESSING_STATUS_SUCCESS = "success"
PROCESSING_STATUS_PARTIAL = "partial"
PROCESSING_STATUS_ERROR = "error"

# Request Validation
MIN_QUERY_LENGTH = 1
MAX_SIMILARITY_THRESHOLD = 1.0
MIN_SIMILARITY_THRESHOLD = 0.0