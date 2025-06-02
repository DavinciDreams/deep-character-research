import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import LoadingScreen from '../components/LoadingScreen';
import ChatMessage from '../components/ChatMessage';

export default function ChatInterface() {
  const { characterName } = useParams();
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [characterImage, setCharacterImage] = useState('');

  useEffect(() => {
    // Simulate loading character data
    const loadCharacter = async () => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      setCharacterImage(`https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Leonardo_self.jpg/800px-Leonardo_self.jpg`);
      setLoading(false);
      // Add welcome message
      setMessages([{
        type: 'character',
        content: `Greetings! I am ${characterName}. What would you like to discuss?`
      }]);
    };

    loadCharacter();
  }, [characterName]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages(prev => [...prev, { type: 'user', content: input }]);
    setInput('');

    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        type: 'character',
        content: `As ${characterName}, I would respond to "${input}" with great wisdom...`
      }]);
    }, 1000);
  };

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white flex">
      {/* Character Info Sidebar */}
      <div className="w-96 border-r border-slate-700 p-6 hidden lg:block">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <div className="relative mb-6">
            <div className="absolute inset-0 bg-gradient-to-b from-amber-500/20 to-transparent rounded-lg blur-sm"></div>
            <img
              src={characterImage}
              alt={characterName}
              className="w-full h-80 object-cover rounded-lg relative z-10"
            />
          </div>
          <h2 className="text-2xl font-bold mb-4">{characterName}</h2>
          <div className="space-y-4 text-slate-300">
            <p>Historical Period: Renaissance</p>
            <p>Known for: Art, Science, Engineering</p>
          </div>
        </motion.div>
      </div>

      {/* Chat Interface */}
      <div className="flex-1 flex flex-col max-h-screen">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} {...message} />
          ))}
        </div>

        <form onSubmit={handleSendMessage} className="p-4 border-t border-slate-700">
          <div className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-amber-500"
            />
            <button
              type="submit"
              className="px-6 py-2 bg-gradient-to-r from-amber-500 to-yellow-500 rounded-lg text-black font-semibold hover:from-amber-400 hover:to-yellow-400 transition-colors"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}