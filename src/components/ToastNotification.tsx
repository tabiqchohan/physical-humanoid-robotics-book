import React, { useEffect } from 'react';
import './ToastNotification.css';

export type ToastType = 'info' | 'success' | 'warning' | 'error';

interface ToastNotificationProps {
  message: string;
  type?: ToastType;
  duration?: number;
  onClose?: () => void;
  className?: string;
}

export const ToastNotification: React.FC<ToastNotificationProps> = ({
  message,
  type = 'info',
  duration = 3000,
  onClose,
  className = ''
}) => {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose?.();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const toastClass = `toast-notification toast-${type} ${className}`;

  return (
    <div className={toastClass}>
      <span className="toast-message">{message}</span>
      <button className="toast-close" onClick={onClose}>
        ×
      </button>
    </div>
  );
};