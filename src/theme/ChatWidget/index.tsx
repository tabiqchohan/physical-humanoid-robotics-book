import React, { useEffect, useState } from 'react';
import { ChatProvider } from '../../contexts/ChatContext';
import { ChatContainer } from '../../components/ChatContainer';
import { SelectedTextBanner } from '../../components/SelectedTextBanner';
import { useTextSelection } from '../../hooks/useTextSelection';
import './styles.css';

const ChatWidget = ({ backendUrl }: { backendUrl?: string }) => {
  const { selectedText } = useTextSelection();
  const [isClient, setIsClient] = useState(false);

  // Ensure widget only renders on client
  useEffect(() => {
    setIsClient(true);
  }, []);

  const finalBackendUrl = backendUrl || "https://tabiqchohan-rag-chatbot.hf.space";

  if (!isClient) return null;

  return (
    <ChatProvider>
      <div className="chat-widget-container" data-backend-url={finalBackendUrl}>
        {selectedText && <SelectedTextBanner />}
        <ChatContainer />
      </div>
    </ChatProvider>
  );
};

export default ChatWidget;
