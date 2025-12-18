import React from 'react';
import ChatWidget from '@theme/ChatWidget';

const Root = ({ children }) => {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
};

export default Root;