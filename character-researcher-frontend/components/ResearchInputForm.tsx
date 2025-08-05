import ChatDialog from './ChatDialog';
// This component will be refactored to a two-stage flow:
// 1. Input character name, then load.
// 2. Show chat dialog for user messages.
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { postResearchQuery } from '../services/api';

const ResearchInputForm: React.FC = () => {
  const [character, setCharacter] = useState('');
  const [loaded, setLoaded] = useState(false);

  if (!loaded) {
    return (
      <form
        onSubmit={e => {
          e.preventDefault();
          if (character.trim()) setLoaded(true);
        }}
      >
        <input
          type="text"
          placeholder="Enter character name..."
          value={character}
          onChange={e => setCharacter(e.target.value)}
          required
          style={{ marginBottom: 8 }}
        />
        <button type="submit" disabled={!character.trim()}>
          Load
        </button>
      </form>
    );
  }

  return <ChatDialog character={character} />;
}



export default ResearchInputForm;