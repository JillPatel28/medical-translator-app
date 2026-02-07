import React, { useState } from 'react';

function TextInput({ onSubmit, isLoading }) {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim()) {
      onSubmit(text);
      setText('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="text-input-container">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message here..."
        disabled={isLoading}
        rows="3"
      />
      <button onClick={handleSubmit} disabled={isLoading || !text.trim()}>
        {isLoading ? 'Sending...' : 'Send'}
      </button>
    </div>
  );
}

export default TextInput;