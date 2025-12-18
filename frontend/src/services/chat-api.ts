import { QueryRequest, QueryResponse } from '../types/chat';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export interface ChatApiService {
  queryFullBook(request: QueryRequest): Promise<QueryResponse>;
  querySelectedText(request: QueryRequest): Promise<QueryResponse>;
  healthCheck(): Promise<boolean>;
}

class ChatApiServiceImpl implements ChatApiService {
  async queryFullBook(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response = await fetch(`${BACKEND_URL}/api/chat/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error querying full book content:', error);
      throw error;
    }
  }

  async querySelectedText(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response = await fetch(`${BACKEND_URL}/api/chat/query-selected-text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error querying selected text content:', error);
      throw error;
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${BACKEND_URL}/api/health`, {
        method: 'GET',
      });

      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

export const chatApiService = new ChatApiServiceImpl();