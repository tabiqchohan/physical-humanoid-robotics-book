import React from 'react';
import './ErrorMessage.css';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  onRetry,
  className = ''
}) => {
  return (
    <div className={`error-message ${className}`}>
      <div className="error-content">
        <span className="error-icon">⚠️</span>
        <span className="error-text">{message}</span>
      </div>
      {onRetry && (
        <button className="error-retry-button" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
};