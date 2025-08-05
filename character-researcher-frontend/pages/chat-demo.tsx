import React from 'react';
import ChatInterface from '../components/ChatInterface';
import { HistoricalFigure } from '../types/types';

const mockFigure: HistoricalFigure = {
  id: 2,
  name: 'Ada Lovelace',
  era: 'Victorian Era',
  years: '1815–1852',
  portraitUrl: 'https://upload.wikimedia.org/wikipedia/commons/a/a4/Ada_Lovelace_portrait.jpg',
  shortDescription: 'English mathematician and writer, known for her work on the Analytical Engine.',
};

const ChatDemoPage = () => (
  <div style={{ maxWidth: 500, margin: '40px auto', background: '#181a1b', borderRadius: 12, boxShadow: '0 2px 16px #0008', padding: 24 }}>
    <ChatInterface
      figure={mockFigure}
      onReturn={() => alert('Return clicked')}
      portalActive={true}
      soundEnabled={true}
    />
  </div>
);

export default ChatDemoPage;