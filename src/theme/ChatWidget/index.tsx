import React, { useEffect, useState } from 'react';
import { ChatProvider } from '../../contexts/ChatContext';
import { ChatContainer } from '../../components/ChatContainer';
import { SelectedTextBanner } from '../../components/SelectedTextBanner';
import { useTextSelection } from '../../hooks/useTextSelection';
import './styles.css';

const ChatWidget = () => {
  const { selectedText } = useTextSelection();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => setIsClient(true), []);

  if (!isClient) return null; // Do not render on server

  const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || "https://tabiqchohan-rag-chatbot.hf.space";

  return (
    <ChatProvider>
      <div className="chat-widget-container" data-backend-url={backendUrl}>
        {selectedText && <SelectedTextBanner />}
        <ChatContainer />
      </div>
    </ChatProvider>
  );
};

export default ChatWidget;
