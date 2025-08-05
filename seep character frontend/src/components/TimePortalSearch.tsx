import React, { useState } from 'react';
import './styles/retro.scss';
import './styles/futuristic.scss';

const TimePortalSearch: React.FC = () => {
    const [query, setQuery] = useState('');

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    };

    const handleSearch = () => {
        // Implement search functionality here
        console.log('Searching for:', query);
    };

    return (
        <div className="time-portal-search">
            <h1 className="portal-title">Enter the Time Portal</h1>
            <input
                type="text"
                value={query}
                onChange={handleInputChange}
                placeholder="Search for characters..."
                className="search-input"
            />
            <button onClick={handleSearch} className="search-button">
                Activate Portal
            </button>
        </div>
    );
};

export default TimePortalSearch;