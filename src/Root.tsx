// src/Root.tsx
import React from "react";
import ChatWidget from '@theme/ChatWidget'; // import only, no declare

type RootProps = {
  children: React.ReactNode;
};

export default function Root({ children }: RootProps) {
  // Backend URL safe fallback
  const backendUrl =
    typeof process !== "undefined" && process.env.REACT_APP_BACKEND_URL
      ? process.env.REACT_APP_BACKEND_URL
      : "https://tabiqchohan-rag-chatbot.hf.space";

  console.log("Chatbot backend URL:", backendUrl);

  return (
    <>
      {children}
      <ChatWidget backendUrl={backendUrl} />
    </>
  );
}
