import React from 'react';
import { useChatContext } from '../contexts/ChatContext';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { SourceCitation } from './SourceCitation';
import styles from './ChatContainer.module.css';

interface ChatContainerProps {
  className?: string;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({ className = '' }) => {
  const { state } = useChatContext();

  return (
    <div className={`${styles.chatContainer} ${className}`}>
      <div className={styles.chatHeader}>
        <h3>RAG Chat Assistant</h3>
      </div>

      <div className={styles.chatMessages}>
        <MessageList />
      </div>

      <div className={styles.chatInput}>
        <MessageInput />
      </div>

      {state.error && (
        <div className={styles.chatError}>
          Error: {state.error}
        </div>
      )}

      {state.isLoading && (
        <div className={styles.chatLoading}>
          Thinking...
        </div>
      )}
    </div>
  );
};
