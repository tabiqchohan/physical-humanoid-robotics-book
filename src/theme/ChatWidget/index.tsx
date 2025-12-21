import React, { useEffect, useState } from 'react';
import { ChatProvider } from '../../contexts/ChatContext';
import { ChatContainer } from '../../components/ChatContainer';
import { SelectedTextBanner } from '../../components/SelectedTextBanner';
import { useTextSelection } from '../../hooks/useTextSelection';
import './styles.css';

const ChatWidget = () => {
  const { selectedText } = useTextSelection();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) return null;

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
