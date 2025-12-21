import { useEffect, useState, useCallback } from 'react';
import { useChatContext } from '../contexts/ChatContext';

export const useTextSelection = () => {
  const { dispatch } = useChatContext();
  const [selectedText, setSelectedText] = useState<string | null>(null);

  const handleSelection = useCallback(() => {
    // Check if running in browser environment
    if (typeof window !== 'undefined' && typeof document !== 'undefined') {
      const selection = window.getSelection();
      const text = selection?.toString().trim() || '';

      if (text) {
        setSelectedText(text);
        dispatch({ type: 'SET_SELECTED_TEXT', payload: text });
      } else {
        setSelectedText(null);
        dispatch({ type: 'SET_SELECTED_TEXT', payload: null });
      }
    }
  }, [dispatch]);

  useEffect(() => {
    // Only add event listeners if in browser environment
    if (typeof window !== 'undefined' && typeof document !== 'undefined') {
      // Add event listeners for text selection
      document.addEventListener('mouseup', handleSelection);
      document.addEventListener('keyup', handleSelection);

      // Cleanup event listeners on unmount
      return () => {
        document.removeEventListener('mouseup', handleSelection);
        document.removeEventListener('keyup', handleSelection);
      };
    }
  }, [handleSelection]);

  const clearSelection = useCallback(() => {
    setSelectedText(null);
    dispatch({ type: 'SET_SELECTED_TEXT', payload: null });

    // Only clear selection if in browser environment
    if (typeof window !== 'undefined' && typeof window.getSelection !== 'undefined') {
      window.getSelection()?.removeAllRanges();
    }
  }, [dispatch]);

  return { selectedText, clearSelection };
};