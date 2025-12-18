import React from 'react';
import { useChatContext } from '../contexts/ChatContext';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { SourceCitation } from './SourceCitation';
import './ChatContainer.css';

interface ChatContainerProps {
  className?: string;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({ className = '' }) => {
  const { state } = useChatContext();

  return (
    <div className={`chat-container ${className}`}>
      <div className="chat-header">
        <h3>RAG Chat Assistant</h3>
      </div>

      <div className="chat-messages">
        <MessageList />
      </div>

      <div className="chat-input">
        <MessageInput />
      </div>

      {state.error && (
        <div className="chat-error">
          Error: {state.error}
        </div>
      )}

      {state.isLoading && (
        <div className="chat-loading">
          Thinking...
        </div>
      )}
    </div>
  );
};