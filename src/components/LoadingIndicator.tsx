import React from 'react';
import './LoadingIndicator.css';

interface LoadingIndicatorProps {
  message?: string;
  className?: string;
}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  message = 'Thinking...',
  className = ''
}) => {
  return (
    <div className={`loading-indicator ${className}`}>
      <div className="loading-content">
        <div className="loading-spinner"></div>
        <span className="loading-message">{message}</span>
      </div>
    </div>
  );
};