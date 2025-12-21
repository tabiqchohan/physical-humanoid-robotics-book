# RAG Chatbot Backend – OpenAI Agent & Retrieval Integration

This project implements a FastAPI backend that exposes RAG (Retrieval-Augmented Generation) functionality for OpenAI Agent SDK integration. The system accepts natural language queries, generates embeddings using Cohere, performs similarity search against Qdrant vector database, and returns structured results with relevant document chunks and metadata.

## Setup

### Prerequisites
- Python 3.12+
- pip package manager
- Access to Cohere API (API key)
- Access to Qdrant vector database (cloud or local instance)

### 1. Install Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the backend directory with the following variables:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=your_collection_name
ENVIRONMENT=development
LOG_LEVEL=INFO
MAX_QUERY_LENGTH=1000
DEFAULT_TOP_K=5
DEFAULT_SIMILARITY_THRESHOLD=0.5
```

## Running the Application

### Start the Server
```bash
cd backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `https://tabiqchohan-rag-chatbot.hf.space` (when deployed) or `http://localhost:8000` (for local development)

### Verify Installation
Check that the server is running:
```bash
curl https://tabiqchohan-rag-chatbot.hf.space/health  # For deployed version
# or
curl http://localhost:8000/health  # For local development
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-17T10:30:00Z"
}
```

## API Endpoints

### Search Endpoint
Send a query to retrieve relevant document chunks:

```bash
curl -X POST https://tabiqchohan-rag-chatbot.hf.space/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the benefits of renewable energy?",
    "top_k": 3,
    "similarity_threshold": 0.5
  }'
# or for local development:
curl -X POST http://localhost:8000/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the benefits of renewable energy?",
    "top_k": 3,
    "similarity_threshold": 0.5
  }'
```

### Validate Endpoint
Validate a query before processing:

```bash
curl -X POST https://tabiqchohan-rag-chatbot.hf.space/retrieval/validate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the benefits of renewable energy?"
  }'
# or for local development:
curl -X POST http://localhost:8000/retrieval/validate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the benefits of renewable energy?"
  }'
```

## Integration with OpenAI Agent SDK

To use this backend with the OpenAI Agent SDK, define a function tool that calls the search endpoint. An example implementation is provided in `examples/openai_agent_integration.py`.

### Basic Integration

```python
import openai
import requests

def search_knowledge_base(query: str, top_k: int = 5) -> dict:
    """
    Search the knowledge base for information related to the query.

    Args:
        query: The natural language query to search for
        top_k: Number of results to return (default: 5)

    Returns:
        Dictionary containing search results
    """
    # For deployed version:
    response = requests.post(
        "https://tabiqchohan-rag-chatbot.hf.space/retrieval/search",
        json={"query": query, "top_k": top_k}
    )
    # For local development, use:
    # response = requests.post(
    #     "http://localhost:8000/retrieval/search",
    #     json={"query": query, "top_k": top_k}
    # )
    return response.json()

# Register the function with OpenAI
functions = [
    {
        "name": "search_knowledge_base",
        "description": "Search the knowledge base for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return"
                }
            },
            "required": ["query"]
        }
    }
]
```

### Using the OpenAI Assistants API

For integration with the OpenAI Assistants API, register the tool during assistant creation:

```python
client = openai.OpenAI(api_key="your-api-key")

assistant = client.beta.assistants.create(
    name="Knowledge Base Assistant",
    instructions="You are a helpful assistant with access to a knowledge base. Use the search_knowledge_base function to find relevant information.",
    model="gpt-4-turbo",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": "Search the knowledge base for information related to the user's query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The natural language query to search for in the knowledge base"
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of results to return",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 10
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]
)
```

### Example Usage

See the complete example in `backend/examples/openai_agent_integration.py` for a full implementation showing:
- How to define the search function as a tool
- How to register the tool with an OpenAI assistant
- How to handle responses from the knowledge base API
- Example interaction flow between agent and knowledge base

## Running Tests

### Unit Tests
```bash
python -m pytest tests/unit/ -v
```

### Integration Tests
```bash
python -m pytest tests/integration/ -v
```

### All Tests
```bash
python -m pytest tests/ -v
```

## Architecture

The backend consists of the following main components:

1. **API Layer**: FastAPI endpoints with request/response validation using Pydantic models
2. **Service Layer**: Business logic for retrieval, embedding generation, and vector database operations
3. **Configuration**: Pydantic settings for environment-based configuration
4. **Utilities**: Helper functions and common utilities

## Features

- FastAPI with automatic OpenAPI documentation
- Cohere embedding integration for semantic search
- Qdrant vector database for efficient similarity search
- Comprehensive request/response validation
- Structured logging with correlation IDs
- Performance monitoring and metrics
- Error handling with appropriate HTTP status codes
- OpenAI Agent SDK compatibility
- Deployable on cloud platforms (Railway, Hugging Face Spaces)

## Deployment

### Railway Deployment
The application is pre-configured for Railway deployment using the provided `Dockerfile` and `Procfile`.

### Hugging Face Spaces Deployment
For Hugging Face Spaces deployment, refer to the `HUGGINGFACE_DEPLOYMENT_GUIDE.md` file for detailed instructions.

The application can be deployed to Hugging Face Spaces using:
- The provided `Dockerfile.hf`
- Environment variables for API keys and configuration
- The `app.py` entry point for Hugging Face compatibility