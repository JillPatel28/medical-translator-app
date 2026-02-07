import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import MessageThread from './components/MessageThread';
import AudioRecorder from './components/AudioRecorder';
import TextInput from './components/TextInput';
import SearchBar from './components/SearchBar';
import SummaryPanel from './components/SummaryPanel';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentRole, setCurrentRole] = useState('doctor');
  const [summary, setSummary] = useState('');
  const [selectedMessages, setSelectedMessages] = useState([]);
  const [error, setError] = useState('');
  const messageEndRef = useRef(null);

  const API_BASE_URL = '/api';

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      setError('');
      const response = await fetch(`${API_BASE_URL}/messages/`);
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.messages && Array.isArray(data.messages)) {
        setMessages(data.messages);
      } else {
        console.warn('[v0] Unexpected message format:', data);
        setMessages([]);
      }
    } catch (error) {
      console.error('[v0] Error fetching messages:', error);
      setError('Failed to load messages');
    }
  };

  const handleTextSubmit = async (text) => {
    if (!text.trim()) return;

    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE_URL}/translate/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: currentRole, text })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.id) {
        const newMessage = {
          id: data.id,
          role: data.role,
          original_text: data.original_text,
          translated_text: data.translated_text,
          timestamp: data.timestamp
        };
        setMessages([...messages, newMessage]);
        setSummary('');
      }
    } catch (error) {
      console.error('[v0] Error translating text:', error);
      setError('Error sending message. Make sure backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAudioSubmit = async (audioBlob) => {
    setIsLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');
      formData.append('role', currentRole);

      const response = await fetch(`${API_BASE_URL}/audio/`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.id) {
        const newMessage = {
          id: data.id,
          role: data.role,
          original_text: data.transcribed_text,
          translated_text: data.translated_text,
          timestamp: data.timestamp
        };
        setMessages([...messages, newMessage]);
        setSummary('');
      }
    } catch (error) {
      console.error('[v0] Error uploading audio:', error);
      setError(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (keyword) => {
    if (!keyword.trim()) {
      fetchMessages();
      return;
    }

    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/search/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keyword })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      if (data.messages && Array.isArray(data.messages)) {
        setMessages(data.messages);
      }
    } catch (error) {
      console.error('[v0] Error searching messages:', error);
      setError('Search failed');
    }
  };

  const handleSummarize = async () => {
    if (selectedMessages.length === 0) return;

    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/summarize/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message_ids: selectedMessages })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      if (data.summary) {
        setSummary(data.summary);
      }
    } catch (error) {
      console.error('[v0] Error summarizing:', error);
      setError('Failed to generate summary');
    }
  };

  const toggleMessageSelection = (messageId) => {
    setSelectedMessages(prev =>
      prev.includes(messageId)
        ? prev.filter(id => id !== messageId)
        : [...prev, messageId]
    );
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Doctor-Patient Translation App</h1>
        <div className="role-selector">
          <button
            className={`role-btn ${currentRole === 'doctor' ? 'active' : ''}`}
            onClick={() => setCurrentRole('doctor')}
          >
            Doctor
          </button>
          <button
            className={`role-btn ${currentRole === 'patient' ? 'active' : ''}`}
            onClick={() => setCurrentRole('patient')}
          >
            Patient
          </button>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <SearchBar onSearch={handleSearch} />

      <MessageThread
        messages={messages}
        selectedMessages={selectedMessages}
        onToggleSelect={toggleMessageSelection}
        messageEndRef={messageEndRef}
      />

      {summary && <SummaryPanel summary={summary} />}

      <div className="input-section">
        <TextInput onSubmit={handleTextSubmit} isLoading={isLoading} />
        <AudioRecorder onSubmit={handleAudioSubmit} isLoading={isLoading} />
      </div>

      {selectedMessages.length > 0 && (
        <div className="summary-controls">
          <button onClick={handleSummarize} disabled={isLoading}>
            Summarize ({selectedMessages.length} selected)
          </button>
          <button onClick={() => setSelectedMessages([])}>Clear Selection</button>
        </div>
      )}
    </div>
  );
}

export default App;