# Deploying RAG Chatbot Backend to Hugging Face Spaces

## Prerequisites

Before deploying, ensure you have:
1. A Hugging Face account
2. Valid API keys for:
   - Cohere API (for embeddings)
   - Qdrant vector database (cloud or self-hosted)
3. A GitHub account to fork the repository

## Existing Space

If you already have an existing space, you can find it at:
- https://huggingface.co/spaces/tabiqchohan/rag-chatbot

Note: This deployment guide assumes you're creating a new space or updating an existing one with the latest backend code.

## Deployment Steps

### Step 1: Fork the Repository

1. Go to the repository on GitHub
2. Click the "Fork" button to create a copy in your GitHub account

### Step 2: Prepare Environment Variables

Before deploying, you'll need these environment variables:
- `COHERE_API_KEY`: Your Cohere API key for embeddings
- `QDRANT_URL`: URL to your Qdrant database (e.g., https://your-cluster.us-east4-0.gcp.cloud.qdrant.io:6333)
- `QDRANT_API_KEY`: Your Qdrant API key (if using cloud version)
- `QDRANT_COLLECTION_NAME`: The name of the collection to query

### Step 3: Create Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create Space"
3. Fill in the form:
   - **Space name**: Choose a unique name for your space
   - **Repository**: Enter your forked repository URL
   - **SDK**: Select "Docker"
   - **License**: Choose an appropriate license
   - **Hardware**: Select "CPU Basic" or higher depending on your needs
   - **Visibility**: Choose "Public" or "Private"

### Step 4: Configure Environment Variables

After creating the Space:

1. Go to your Space page
2. Click on "Files" tab
3. Click on "Environment" or "Secrets" (depending on your Hugging Face interface)
4. Add the following environment variables:
   - `COHERE_API_KEY` = [your_cohere_api_key]
   - `QDRANT_URL` = [your_qdrant_url]
   - `QDRANT_API_KEY` = [your_qdrant_api_key]
   - `QDRANT_COLLECTION_NAME` = [your_collection_name]

### Step 5: Verify Deployment

1. Check the "Logs" tab to see the build and startup process
2. Wait for the status to show "Running"
3. The application will be available at: `https://[your-username]-[space-name].hf.space`

## Alternative: Manual Docker Deployment

If you prefer to customize the deployment:

### Using the Provided Dockerfile.hf

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

## API Usage

Once deployed, you can access the following endpoints:

### Health Check
```
GET /
```

### Semantic Search
```
POST /retrieval/search
Content-Type: application/json

{
  "query": "your search query",
  "top_k": 5,
  "similarity_threshold": 0.5
}
```

### Query Validation
```
POST /retrieval/validate
Content-Type: application/json

{
  "query": "your query to validate"
}
```

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check that all dependencies in requirements.txt are compatible
2. **Runtime Errors**: Verify all environment variables are set correctly
3. **Port Issues**: Ensure the application binds to port 7860
4. **API Key Issues**: Confirm API keys have proper permissions and are not expired

### Logs:
- Check the "Logs" tab in your Space for startup and runtime information
- Look for specific error messages that can help identify issues

## Scaling and Performance

- For high-traffic applications, consider upgrading to higher hardware tiers
- Monitor the Space's resource usage and adjust accordingly
- Consider caching strategies for frequently accessed data

## Security Considerations

- Keep API keys secure and never expose them in client-side code
- Use HTTPS endpoints for all API calls
- Regularly rotate API keys
- Monitor usage patterns for unusual activity