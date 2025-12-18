import React from 'react';
import { useChatContext } from '../contexts/ChatContext';
import './SelectedTextBanner.css';

export const SelectedTextBanner: React.FC = () => {
  const { state } = useChatContext();

  if (!state.selectedText) {
    return null;
  }

  return (
    <div className="selected-text-banner">
      <div className="selected-text-content">
        <strong>Selected Text:</strong> {state.selectedText.substring(0, 100)}...
      </div>
      <button
        className="clear-selection-button"
        onClick={() => {
          // In a real implementation, we would clear the selected text from context
          console.log('Clearing selected text');
        }}
      >
        Clear
      </button>
    </div>
  );
};