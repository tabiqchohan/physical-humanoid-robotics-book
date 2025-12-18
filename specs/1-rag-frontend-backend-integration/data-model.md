# Data Model: RAG Chatbot Frontend-Backend Integration

## Overview
This document defines the data models for the RAG chatbot integration between Docusaurus frontend and FastAPI backend.

## Frontend Data Models

### ChatSession
- **sessionId**: string (unique identifier for the session)
- **messages**: Message[] (array of messages in the conversation)
- **createdAt**: Date (timestamp when session was created)
- **lastActiveAt**: Date (timestamp of last activity)
- **selectedTextContext**: string | null (optional text that was selected when session started)

### Message
- **id**: string (unique identifier for the message)
- **content**: string (the actual message content)
- **sender**: 'user' | 'assistant' (indicates who sent the message)
- **timestamp**: Date (when the message was created)
- **sources**: SourceReference[] (optional array of source references from RAG response)
- **context**: string | null (optional context from selected text)

### SourceReference
- **title**: string (title of the source document/page)
- **url**: string (URL to the source)
- **content**: string (relevant excerpt from the source)
- **confidence**: number (confidence score from RAG system)

### ChatState
- **isLoading**: boolean (indicates if a response is being processed)
- **error**: string | null (error message if any)
- **currentQuery**: string | null (the current query being processed)
- **selectedText**: string | null (currently selected text on the page)

## Backend Data Models

### QueryRequest
- **query**: string (the user's question)
- **context**: string | null (optional context from selected text)
- **sessionId**: string | null (optional session identifier for conversation history)
- **userId**: string | null (optional user identifier)

### QueryResponse
- **response**: string (the AI-generated response)
- **sources**: SourceMetadata[] (array of sources used to generate the response)
- **sessionId**: string (session identifier for conversation continuity)
- **timestamp**: string (ISO date string for the response)

### SourceMetadata
- **title**: string (title of the source document)
- **url**: string (URL to the source location)
- **content**: string (relevant excerpt from the source)
- **score**: number (relevance score from vector search)
- **page**: number | null (page number if applicable)

## API Contract

### POST /api/chat/query
**Description**: Submit a query to the RAG system
**Request**:
```json
{
  "query": "What are the key principles of Physical AI?",
  "context": "Selected text context if applicable",
  "sessionId": "session-123"
}
```
**Response**:
```json
{
  "response": "The key principles of Physical AI include...",
  "sources": [
    {
      "title": "Physical AI Principles",
      "url": "/docs/physical-ai/principles",
      "content": "Excerpt from the source...",
      "score": 0.92,
      "page": 15
    }
  ],
  "sessionId": "session-123",
  "timestamp": "2025-12-18T10:30:00Z"
}
```

### POST /api/chat/query-selected-text
**Description**: Submit a query specifically about selected text
**Request**:
```json
{
  "query": "Can you explain this concept?",
  "context": "The specific text that was selected by the user",
  "sessionId": "session-123"
}
```
**Response**: Same as /api/chat/query

### GET /api/chat/health
**Description**: Check the health of the RAG system
**Response**:
```json
{
  "status": "healthy",
  "backend": "available",
  "vector_db": "connected",
  "timestamp": "2025-12-18T10:30:00Z"
}
```

## Validation Rules

### Message
- content must be 1-2000 characters
- sender must be either 'user' or 'assistant'
- timestamp must be a valid date

### QueryRequest
- query must be 1-1000 characters
- context, if provided, must be 1-5000 characters
- sessionId, if provided, must match UUID format

### SourceReference/SourceMetadata
- title must be 1-200 characters
- url must be a valid URL format
- content must be 1-10000 characters
- score/confidence must be between 0 and 1

## State Transitions

### ChatSession
- Created → Active (when first message is sent)
- Active → Inactive (after 30 minutes of inactivity)
- Inactive → Archived (after 24 hours of inactivity)

### Message
- Created → Processing (when sent to backend)
- Processing → Completed (when response received)
- Processing → Error (when backend error occurs)