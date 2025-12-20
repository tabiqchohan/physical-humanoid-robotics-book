# Railway Deployment Guide for RAG Chatbot Backend

This guide explains how to deploy the RAG Chatbot backend to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app) if you don't have an account
2. **API Keys**: You'll need the following API keys:
   - Cohere API Key (for embeddings)
   - Qdrant API Key and URL (for vector database)

## Deployment Steps

### 1. Connect Your GitHub Repository (Recommended)

1. Fork or push this repository to GitHub if you haven't already
2. Go to [railway.app](https://railway.app) and sign in
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository containing this backend code
5. Railway will automatically detect the Dockerfile and deploy configuration

### 2. Manual Deployment via Railway CLI

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   # or
   curl -fsSL https://railway.app/install.sh | bash
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Link your project:
   ```bash
   cd backend
   railway init
   ```

4. Deploy:
   ```bash
   railway up
   ```

### 3. Configure Environment Variables

After deployment, you need to set the following environment variables in Railway:

1. Go to your Railway project dashboard
2. Navigate to the "Variables" section
3. Add the following variables:

```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=rag_embeddings
ENVIRONMENT=production
LOG_LEVEL=INFO
MAX_QUERY_LENGTH=1000
DEFAULT_TOP_K=5
DEFAULT_SIMILARITY_THRESHOLD=0.5
```

## Application Structure

The backend is built with:
- **FastAPI** as the web framework
- **Cohere** for text embeddings
- **Qdrant** as the vector database
- **Python 3.12** runtime

## API Endpoints

Once deployed, your API will be available at:
- Health check: `https://<your-app-name>.up.railway.app/health`
- Chat endpoint: `https://<your-app-name>.up.railway.app/api/chat/query`
- Documentation: `https://<your-app-name>.up.railway.app/docs`

## Configuration Details

### Dockerfile
- Uses Python 3.12-slim base image
- Installs system dependencies (gcc for Python packages)
- Copies requirements first for better caching
- Runs with uvicorn server on PORT environment variable

### railway.toml
- Uses Docker builder
- Sets start command to run FastAPI with uvicorn
- Configures deployment settings

### Procfile
- Defines web process for compatibility with multiple platforms

## Environment Variables Explained

- `COHERE_API_KEY`: Required for generating text embeddings
- `QDRANT_URL`: URL to your Qdrant vector database instance
- `QDRANT_API_KEY`: API key for authenticating with Qdrant
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings (default: rag_embeddings)
- `ENVIRONMENT`: Set to "production" for deployed instances
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR, etc.)
- `MAX_QUERY_LENGTH`: Maximum allowed query length in characters
- `DEFAULT_TOP_K`: Default number of results to return
- `DEFAULT_SIMILIARY_THRESHOLD`: Minimum similarity threshold for results

## Scaling

Railway allows you to scale your application:
1. Go to your project dashboard
2. Navigate to the "Deployments" section
3. Adjust the number of replicas as needed

## Monitoring

- Check logs in the Railway dashboard under "Logs" section
- Monitor resource usage in the "Metrics" section
- Set up alerts for critical issues

## Troubleshooting

### Common Issues:

1. **Application crashes on startup**: Check that all required environment variables are set
2. **Database connection errors**: Verify QDRANT_URL and QDRANT_API_KEY are correct
3. **Embedding errors**: Ensure COHERE_API_KEY is valid and has sufficient quota

### Logs Access:
```bash
railway logs
```

## Next Steps

After successful deployment:
1. Test the health endpoint to ensure the application is running
2. Test the chat endpoint with sample queries
3. Integrate with your frontend application
4. Set up a custom domain if desired

## Security Considerations

- Never commit API keys to version control
- Use Railway's secure environment variables for sensitive data
- Consider restricting CORS origins in production (currently set to "*")
- Monitor API usage and set appropriate rate limits