import React, { useEffect, useState } from "react";
import ChatWidget from '@theme/ChatWidget';

type RootProps = { children: React.ReactNode };

export default function Root({ children }: RootProps) {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => setIsClient(true), []);

  return (
    <>
      {children}
      {isClient && <ChatWidget />}
    </>
  );
}
