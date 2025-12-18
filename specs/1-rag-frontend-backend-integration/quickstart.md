# Quickstart Guide: RAG Chatbot Integration

## Overview
This guide provides instructions for setting up and running the RAG chatbot integration with Docusaurus frontend and FastAPI backend.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Docker (optional, for containerized development)
- Git

## Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the backend server**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend  # or if integrated in root: cd .
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API endpoint configuration
   ```

4. **Start the Docusaurus development server**
   ```bash
   npm start
   ```

## API Endpoints

The RAG chatbot exposes the following API endpoints:

- `POST /api/chat/query` - Submit general queries to the RAG system
- `POST /api/chat/query-selected-text` - Submit queries about selected text
- `GET /api/chat/health` - Health check for the RAG system

## Configuration

### Frontend Configuration
The chat component can be configured via environment variables:

- `REACT_APP_API_BASE_URL` - Base URL for the backend API
- `REACT_APP_DEFAULT_MODEL` - Default model to use for queries (optional)

### Backend Configuration
Configure the backend via environment variables:

- `QDRANT_URL` - URL for the Qdrant vector database
- `QDRANT_API_KEY` - API key for Qdrant (if required)
- `COHERE_API_KEY` - API key for Cohere embeddings
- `OPENAI_API_KEY` - API key for OpenAI (if using OpenAI models)

## Development

### Running Tests
Backend tests:
```bash
cd backend
python -m pytest tests/
```

Frontend tests:
```bash
cd frontend
npm test
```

### Building for Production
Backend:
```bash
cd backend
python -m build
```

Frontend:
```bash
cd frontend
npm run build
```

## Deployment

### GitHub Pages Configuration
For deployment to GitHub Pages:

1. Build the frontend:
   ```bash
   npm run build
   ```

2. Configure the base URL in `docusaurus.config.js`:
   ```js
   module.exports = {
     // ...
     baseUrl: '/your-repo-name/',
     // ...
   };
   ```

3. Set the API endpoint to your deployed backend in the build environment.

### Local Development
For local development, the frontend and backend can run on different ports:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

Configure CORS appropriately in the backend settings.