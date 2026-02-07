import React from 'react';
import MessageBubble from './MessageBubble';

function MessageThread({ messages, selectedMessages, onToggleSelect, messageEndRef }) {
  if (!messages || messages.length === 0) {
    return (
      <div className="message-thread">
        <p className="no-messages">No messages yet. Start a conversation!</p>
      </div>
    );
  }

  return (
    <div className="message-thread">
      {messages.map((msg) => {
        if (!msg || !msg.id) {
          console.warn('[v0] Invalid message structure:', msg);
          return null;
        }

        return (
          <div
            key={msg.id}
            className={`message-item ${selectedMessages.includes(msg.id) ? 'selected' : ''}`}
            onClick={() => onToggleSelect(msg.id)}
          >
            <input 
              type="checkbox" 
              checked={selectedMessages.includes(msg.id)} 
              readOnly 
              onClick={(e) => e.stopPropagation()}
            />
            <MessageBubble
              role={msg.role}
              originalText={msg.original_text}
              translatedText={msg.translated_text}
              timestamp={msg.timestamp}
            />
          </div>
        );
      })}
      <div ref={messageEndRef} />
    </div>
  );
}

export default MessageThread;