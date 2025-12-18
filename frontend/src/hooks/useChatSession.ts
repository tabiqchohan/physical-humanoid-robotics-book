import { useState, useEffect } from 'react';
import { ChatSession, Message } from '../types/chat';

const SESSION_STORAGE_KEY = 'rag-chat-session';

export const useChatSession = () => {
  const [session, setSession] = useState<ChatSession | null>(null);

  // Load session from localStorage on component mount
  useEffect(() => {
    const savedSession = loadSession();
    if (savedSession) {
      setSession(savedSession);
    } else {
      // Create a new session if none exists
      const newSession: ChatSession = {
        sessionId: generateSessionId(),
        messages: [],
        createdAt: new Date(),
        lastActiveAt: new Date(),
      };
      saveSession(newSession);
      setSession(newSession);
    }
  }, []);

  const saveSession = (session: ChatSession) => {
    try {
      const sessionToSave = {
        ...session,
        createdAt: session.createdAt.toISOString(),
        lastActiveAt: session.lastActiveAt.toISOString(),
      };
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(sessionToSave));
    } catch (error) {
      console.error('Failed to save session to localStorage:', error);
    }
  };

  const loadSession = (): ChatSession | null => {
    try {
      const sessionData = localStorage.getItem(SESSION_STORAGE_KEY);
      if (sessionData) {
        const parsed = JSON.parse(sessionData);
        return {
          ...parsed,
          createdAt: new Date(parsed.createdAt),
          lastActiveAt: new Date(parsed.lastActiveAt),
        };
      }
    } catch (error) {
      console.error('Failed to load session from localStorage:', error);
    }
    return null;
  };

  const updateSession = (updates: Partial<ChatSession>) => {
    if (session) {
      const updatedSession = {
        ...session,
        ...updates,
        lastActiveAt: new Date(), // Always update last active time
      };
      setSession(updatedSession);
      saveSession(updatedSession);
    }
  };

  const addMessage = (message: Message) => {
    if (session) {
      const updatedMessages = [...session.messages, message];
      updateSession({ messages: updatedMessages });
    }
  };

  const clearSession = () => {
    localStorage.removeItem(SESSION_STORAGE_KEY);
    const newSession: ChatSession = {
      sessionId: generateSessionId(),
      messages: [],
      createdAt: new Date(),
      lastActiveAt: new Date(),
    };
    saveSession(newSession);
    setSession(newSession);
  };

  return {
    session,
    updateSession,
    addMessage,
    clearSession,
  };
};

// Helper function to generate a unique session ID
const generateSessionId = (): string => {
  return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};