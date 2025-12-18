import React, { useEffect } from 'react';
import { ChatProvider } from '../../contexts/ChatContext';
import { ChatContainer } from '../../components/ChatContainer';
import { SelectedTextBanner } from '../../components/SelectedTextBanner';
import { useTextSelection } from '../../hooks/useTextSelection';
import './styles.css';

const ChatWidget = () => {
  const { selectedText } = useTextSelection();

  return (
    <ChatProvider>
      <div className="chat-widget-container">
        {selectedText && <SelectedTextBanner />}
        <ChatContainer />
      </div>
    </ChatProvider>
  );
};

export default ChatWidget;