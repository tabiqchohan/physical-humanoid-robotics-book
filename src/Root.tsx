import React, { useEffect, useState } from "react";
import ChatWidget from '@theme/ChatWidget';

type RootProps = {
  children: React.ReactNode;
};

export default function Root({ children }: RootProps) {
  const [isClient, setIsClient] = useState(false);

  // Ensure widget only renders on client (browser)
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Backend URL fallback
  const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || "https://tabiqchohan-rag-chatbot.hf.space";

  return (
    <>
      {children}
      {isClient && <ChatWidget backendUrl={backendUrl} />}
    </>
  );
}
