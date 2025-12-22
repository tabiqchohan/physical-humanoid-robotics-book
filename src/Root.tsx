import React, { useState, useEffect, lazy, Suspense } from "react";

type RootProps = { children: React.ReactNode };

const ClientChatWidget = () => {
  const [ChatWidget, setChatWidget] = useState<React.ComponentType | null>(null);

  useEffect(() => {
    // Dynamically import ChatWidget only on the client
    import('@theme/ChatWidget').then(module => {
      setChatWidget(() => module.default);
    });
  }, []);

  if (ChatWidget) {
    return <ChatWidget />;
  }
  return null; // Don't render anything during SSR
};

export default function Root({ children }: RootProps) {
  return (
    <>
      {children}
      <ClientChatWidget />
    </>
  );
}
