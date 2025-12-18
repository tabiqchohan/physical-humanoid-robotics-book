import React from 'react';
import { useChatContext } from '../contexts/ChatContext';
import { SourceCitation } from './SourceCitation';
import './MessageList.css';

export const MessageList: React.FC = () => {
  const { state } = useChatContext();

  return (
    <div className="message-list">
      {state.messages.map((message) => (
        <div
          key={message.id}
          className={`message message-${message.sender}`}
        >
          <div className="message-content">
            {message.content}
          </div>
          {message.sender === 'assistant' && message.sources && message.sources.length > 0 && (
            <div className="message-sources">
              {message.sources.map((source, index) => (
                <SourceCitation key={`${message.id}-source-${index}`} source={source} />
              ))}
            </div>
          )}
        </div>
      ))}
      {state.currentQuery && (
        <div className="message message-user">
          <div className="message-content">
            {state.currentQuery}
          </div>
        </div>
      )}
    </div>
  );
};