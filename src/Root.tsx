// src/Root.tsx
import React from "react";
import ChatWidget from '@theme/ChatWidget';

type RootProps = {
  children: React.ReactNode;
};

export default function Root({ children }: RootProps) {
  // Backend URL safe, TypeScript friendly
  const backendUrl =
    import.meta.env.REACT_APP_BACKEND_URL || "https://tabiqchohan-rag-chatbot.hf.space";

  console.log("Chatbot backend URL:", backendUrl);

  return (
    <>
      {children}
      <ChatWidget backendUrl={backendUrl} />
    </>
  );
}
