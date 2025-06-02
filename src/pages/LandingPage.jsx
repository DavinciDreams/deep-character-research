import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function LandingPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/chat/${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-2xl w-full text-center"
      >
        <h1 className="text-6xl font-bold mb-8 bg-gradient-to-r from-amber-200 to-yellow-500 text-transparent bg-clip-text">
          Time Portal
        </h1>
        <p className="text-xl mb-12 text-slate-300">
          Journey through time to converse with history's greatest minds
        </p>
        
        <form onSubmit={handleSearch} className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-amber-500/20 to-yellow-500/20 rounded-lg blur"></div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Enter a historical figure's name..."
            className="w-full px-6 py-4 bg-slate-800/50 border border-amber-500/30 rounded-lg text-lg placeholder-slate-400 relative z-10 focus:outline-none focus:border-amber-500"
          />
          <button
            type="submit"
            className="mt-6 px-8 py-3 bg-gradient-to-r from-amber-500 to-yellow-500 rounded-lg text-black font-semibold hover:from-amber-400 hover:to-yellow-400 transition-colors"
          >
            Begin Time Travel
          </button>
        </form>

        <div className="mt-16 grid grid-cols-2 md:grid-cols-3 gap-4 text-sm text-slate-400">
          <div className="p-4 border border-slate-700 rounded-lg">
            Leonardo da Vinci
          </div>
          <div className="p-4 border border-slate-700 rounded-lg">
            Marie Curie
          </div>
          <div className="p-4 border border-slate-700 rounded-lg">
            Albert Einstein
          </div>
        </div>
      </motion.div>
    </div>
  );
}