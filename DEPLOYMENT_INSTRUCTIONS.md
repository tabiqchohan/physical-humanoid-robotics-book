# Deployment Instructions for RAG Chatbot

## Overview
This project consists of two parts:
1. **Frontend**: Docusaurus-based documentation site with chat widget
2. **Backend**: FastAPI-based RAG (Retrieval-Augmented Generation) service

Both components need to be deployed separately, and the frontend needs to be configured to connect to the backend.

## Backend Deployment

### Option 1: Deploy to Railway (Recommended)
1. Navigate to the `backend` directory
2. Create a new project on Railway: https://railway.app/
3. Connect your GitHub repository
4. Set the following environment variables in Railway:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant database URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `PORT`: 8000 (or as required by Railway)

### Option 2: Deploy to Heroku
1. Navigate to the `backend` directory
2. Create a new app on Heroku
3. Set the same environment variables as above
4. Deploy using Git or GitHub integration

### Option 3: Deploy to Vercel (Functions)
1. You can also deploy the backend using Vercel's serverless functions
2. Follow Vercel's documentation for Python FastAPI deployment

## Frontend Deployment

### Deploy to Vercel
1. Navigate to the project root directory
2. Deploy the Docusaurus site to Vercel
3. **Important**: Set the environment variable in Vercel dashboard:
   - `REACT_APP_BACKEND_URL`: The full URL of your deployed backend (e.g., `https://your-backend-app-production.up.railway.app`)

## Configuration

### Environment Variables

**Backend (.env in backend directory):**
```
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
PORT=8000
```

**Frontend (set in Vercel dashboard):**
```
REACT_APP_BACKEND_URL=https://your-deployed-backend-url.com
```

## Important Notes

1. The backend API routes have been fixed to include the chat endpoints (`/api/chat/query` and `/api/chat/query-selected-text`)

2. The backend must be deployed before configuring the frontend

3. CORS is enabled in the backend to allow requests from the frontend

4. After deploying both services, the chatbot should appear and function properly on your Vercel-hosted documentation site

## Troubleshooting

If the chatbot still doesn't appear:
1. Check browser console for JavaScript errors
2. Verify that the backend is accessible at the configured URL
3. Test the backend health endpoint: `GET /health`
4. Ensure the backend API endpoints are working: `POST /api/chat/query`

## Example Deployment Flow

1. Deploy backend to Railway → Get backend URL
2. Set `REACT_APP_BACKEND_URL` in Vercel to the backend URL
3. Redeploy frontend to Vercel
4. Chatbot should now work on the deployed site