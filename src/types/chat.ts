// Frontend data models for the RAG chatbot

export interface SourceReference {
  title: string;           // title of the source document/page
  url: string;             // URL to the source
  content: string;         // relevant excerpt from the source
  confidence: number;      // confidence score from RAG system
}

export interface Message {
  id: string;              // unique identifier for the message
  content: string;         // the actual message content
  sender: 'user' | 'assistant'; // indicates who sent the message
  timestamp: Date;         // when the message was created
  sources?: SourceReference[]; // optional array of source references from RAG response
  context?: string | null; // optional context from selected text
}

export interface ChatSession {
  sessionId: string;       // unique identifier for the session
  messages: Message[];     // array of messages in the conversation
  createdAt: Date;         // timestamp when session was created
  lastActiveAt: Date;      // timestamp of last activity
  selectedTextContext?: string | null; // optional text that was selected when session started
}

export interface ChatState {
  isLoading: boolean;      // indicates if a response is being processed
  error: string | null;    // error message if any
  currentQuery?: string | null; // the current query being processed
  selectedText?: string | null; // currently selected text on the page
  messages: Message[];     // array of messages in the conversation
}