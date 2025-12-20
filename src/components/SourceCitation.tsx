import React from 'react';
import { SourceReference } from '../types/chat';
import './SourceCitation.css';

interface SourceCitationProps {
  source: SourceReference;
}

export const SourceCitation: React.FC<SourceCitationProps> = ({ source }) => {
  return (
    <div className="source-citation">
      <div className="source-title">
        <a href={source.url} target="_blank" rel="noopener noreferrer">
          {source.title}
        </a>
      </div>
      <div className="source-content">{source.content.substring(0, 150)}...</div>
      <div className="source-confidence">Confidence: {(source.confidence * 100).toFixed(1)}%</div>
    </div>
  );
};