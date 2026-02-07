import React, { useState } from 'react';

function SearchBar({ onSearch }) {
  const [keyword, setKeyword] = useState('');

  const handleSearch = () => {
    onSearch(keyword);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleClear = () => {
    setKeyword('');
    onSearch('');
  };

  return (
    <div className="search-bar-container">
      <input
        type="text"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Search messages..."
      />
      <button onClick={handleSearch}>Search</button>
      <button onClick={handleClear} className="clear-btn">Clear</button>
    </div>
  );
}

export default SearchBar;