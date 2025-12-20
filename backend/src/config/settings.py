from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # API Configuration
    environment: str = "development"
    log_level: str = "INFO"
    max_query_length: int = 1000
    default_top_k: int = 5
    default_similarity_threshold: float = 0.5

    # Cohere Configuration
    cohere_api_key: str
    cohere_model: str = "embed-multilingual-v3.0"

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "documents"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # App Information
    app_name: str = "RAG Retrieval Validation API"
    app_version: str = "1.0.0"
    debug: bool = True

    model_config = {"env_file": ".env", "env_prefix": "", "case_sensitive": False}


# Create a single instance of settings
settings = Settings()