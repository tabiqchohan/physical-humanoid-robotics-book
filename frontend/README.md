# RAG Chatbot Frontend

This is the frontend component for the RAG Chatbot integrated with Docusaurus.

## Features

- Chat interface for querying the Physical AI & Humanoid Robotics book
- Support for full book content queries
- Support for selected text context queries
- Source citations with confidence scores
- Loading and error states
- Session persistence using localStorage

## Components

- `ChatContainer`: Main chat interface container
- `MessageList`: Displays conversation history
- `MessageInput`: Input field for user queries
- `SourceCitation`: Shows source references for RAG responses
- `SelectedTextBanner`: Shows selected text context
- `LoadingIndicator`: Loading state indicator
- `ErrorMessage`: Error display component
- `ToastNotification`: System-level alerts

## Services

- `chat-api.ts`: Service for communicating with the backend API

## Contexts and Hooks

- `ChatContext`: State management for the chat interface
- `useTextSelection`: Hook for detecting text selection
- `useChatSession`: Hook for session persistence

## Installation

```bash
npm install
```

## Usage

The chat widget is designed to be integrated into Docusaurus documentation pages via the custom theme component at `src/theme/ChatWidget`.

## Environment Variables

- `REACT_APP_BACKEND_URL`: URL of the backend API (default: http://localhost:8000)