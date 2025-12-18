import { useEffect, useState, useCallback } from 'react';
import { useChatContext } from '../contexts/ChatContext';

export const useTextSelection = () => {
  const { dispatch } = useChatContext();
  const [selectedText, setSelectedText] = useState<string | null>(null);

  const handleSelection = useCallback(() => {
    const selection = window.getSelection();
    const text = selection?.toString().trim() || '';

    if (text) {
      setSelectedText(text);
      dispatch({ type: 'SET_SELECTED_TEXT', payload: text });
    } else {
      setSelectedText(null);
      dispatch({ type: 'SET_SELECTED_TEXT', payload: null });
    }
  }, [dispatch]);

  useEffect(() => {
    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Cleanup event listeners on unmount
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [handleSelection]);

  const clearSelection = useCallback(() => {
    setSelectedText(null);
    dispatch({ type: 'SET_SELECTED_TEXT', payload: null });

    // Clear the actual browser selection
    if (window.getSelection) {
      window.getSelection()?.removeAllRanges();
    }
  }, [dispatch]);

  return { selectedText, clearSelection };
};