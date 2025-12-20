# RAG Chatbot Backend - Hugging Face Deployment

This is the FastAPI backend for a RAG (Retrieval-Augmented Generation) chatbot system, configured for deployment on Hugging Face Spaces.

## Overview

This backend provides:
- FastAPI endpoints for semantic search and retrieval
- Integration with Cohere for embeddings
- Qdrant vector database for similarity search
- OpenAI Agent SDK compatibility

## Deployment on Hugging Face Spaces

### Method 1: Direct Space Creation (Recommended)

1. Fork this repository to your GitHub account
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
3. Click "Create Space"
4. Choose the following settings:
   - **SDK**: Docker
   - **License**: Select appropriate license
   - **Hardware**: CPU (or higher if needed)
   - **Repository**: Use your forked repository URL
5. Add the following environment variables in the Space settings:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant database URL
   - `QDRANT_API_KEY`: Your Qdrant API key (if using cloud)
   - `QDRANT_COLLECTION_NAME`: Name of your collection

### Method 2: Using the Dockerfile

If you want to customize the deployment further, you can use the provided Dockerfile:

```Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 7860 which is commonly used by Hugging Face Spaces
EXPOSE 7860

# Run the application with uvicorn on port 7860
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

## Required Environment Variables

The following environment variables must be set for the application to work:

- `COHERE_API_KEY`: API key for Cohere embedding service
- `QDRANT_URL`: URL for your Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if using cloud instance)
- `QDRANT_COLLECTION_NAME`: Name of the collection to search

## API Endpoints

Once deployed, the following endpoints will be available:

- `/health`: Health check endpoint
- `/retrieval/search`: Semantic search endpoint
- `/retrieval/validate`: Query validation endpoint

## Configuration

The application uses Pydantic Settings for configuration. Additional settings can be configured via environment variables:

- `ENVIRONMENT`: Set to "production" for production deployments
- `LOG_LEVEL`: Set logging level (default: INFO)
- `MAX_QUERY_LENGTH`: Maximum query length (default: 1000)
- `DEFAULT_TOP_K`: Default number of results to return (default: 5)

## Troubleshooting

1. **Port Issues**: Make sure the application runs on port 7860 as expected by Hugging Face Spaces
2. **Environment Variables**: Ensure all required environment variables are set in the Space settings
3. **Dependencies**: Check that all dependencies in requirements.txt are compatible with the Hugging Face environment
4. **API Keys**: Verify that your Cohere and Qdrant API keys are valid and have the necessary permissions

## Local Testing

To test the application locally before deployment:

```bash
cd backend
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 7860
```