import React from 'react';

function SummaryPanel({ summary }) {
  return (
    <div className="summary-panel">
      <h3>Conversation Summary</h3>
      <div className="summary-content">{summary}</div>
    </div>
  );
}

export default SummaryPanel;