import React from 'react';

function MessageBubble({ role, originalText, translatedText, timestamp }) {
  const isDoctor = role === 'doctor';
  
  const formatTime = (timestamp) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return 'Just now';
    }
  };

  return (
    <div className={`message-bubble ${isDoctor ? 'doctor' : 'patient'}`}>
      <div className="message-header">
        <span className="role-badge">{role ? role.toUpperCase() : 'USER'}</span>
        <span className="timestamp">{formatTime(timestamp)}</span>
      </div>
      <div className="message-section">
        <div className="label">Original:</div>
        <div className="message-content">{originalText || 'No text'}</div>
      </div>
      {translatedText && (
        <div className="message-section">
          <div className="label">Translation:</div>
          <div className="message-translation">{translatedText}</div>
        </div>
      )}
    </div>
  );
}

export default MessageBubble;