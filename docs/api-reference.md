# API Reference for RAG Chatbot

## Overview

The RAG Chatbot backend provides RESTful API endpoints for querying documentation content using Retrieval Augmented Generation (RAG).

## Base URL

All API endpoints are prefixed with `/api`.

## Rate Limiting

All endpoints are rate-limited to 10 requests per minute per IP address.

## Endpoints

### POST /api/chat/query

Submit a query to search across the full book content.

#### Request Body

```json
{
  "query": "What are the principles of Physical AI?",
  "context": "Optional selected text context",
  "sessionId": "Optional session ID",
  "userId": "Optional user ID"
}
```

#### Response

```json
{
  "response": "The AI-generated response to your query",
  "sources": [
    {
      "title": "Source Title",
      "url": "/docs/source-url",
      "content": "Relevant excerpt from the source",
      "score": 0.85,
      "page": 15
    }
  ],
  "sessionId": "session-123",
  "timestamp": "2025-12-18T10:30:00Z"
}
```

### POST /api/chat/query-selected-text

Submit a query specifically about selected text.

#### Request Body

Same as `/api/chat/query`, but `context` field is required.

#### Response

Same as `/api/chat/query`.

### GET /api/health

Check the health status of the RAG system.

#### Response

```json
{
  "status": "healthy",
  "backend": "available",
  "vector_db": "connected",
  "timestamp": "2025-12-18T10:30:00Z"
}
```

## Error Handling

- `400 Bad Request`: Invalid request parameters
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error during query processing

## Query Validation

- Query text must be 1-1000 characters
- Context, if provided, must be 1-5000 characters
- Session ID, if provided, should match UUID format