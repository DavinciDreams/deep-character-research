import React, { useState } from 'react';
import { sendChatMessage } from '../services/api';

interface ChatDialogProps {
  character: string;
}

const ChatDialog: React.FC<ChatDialogProps> = ({ character }) => {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages(prev => [...prev, { sender: 'user', text: input }]);
    setLoading(true);
    setError(null);
    try {
      const data = await sendChatMessage(character, input);
      setMessages(prev => [...prev, { sender: 'character', text: data.response }]);
    } catch (err: any) {
      setError(err.message || 'Failed to get response.');
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <div>
      <h2>Chat with {character}</h2>
      <div style={{ minHeight: 200, border: '1px solid #ccc', padding: 8, marginBottom: 8 }}>
        {messages.length === 0 && <div style={{ color: '#888' }}>No messages yet.</div>}
        {messages.map((msg, idx) => (
          <div key={idx} style={{ margin: '4px 0', textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <b>{msg.sender === 'user' ? 'You' : character}:</b> {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSend} style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={`Say something to ${character}...`}
          style={{ flex: 1 }}
          disabled={loading}
        />
        <button type="submit" disabled={!input.trim() || loading}>Send</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  );
};

export default ChatDialog;