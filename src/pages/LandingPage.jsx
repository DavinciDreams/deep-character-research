import React, { useState } from 'react';
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
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 bg-time-pattern opacity-10"></div>
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-amber-500/5 to-transparent animate-time-pulse"></div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-2xl w-full text-center relative z-10"
      >
        {/* Decorative gears */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute -top-20 -left-20 w-40 h-40 border-4 border-amber-500/20 rounded-full"
        />
        <motion.div
          animate={{ rotate: -360 }}
          transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
          className="absolute -bottom-16 -right-16 w-32 h-32 border-4 border-yellow-500/20 rounded-full"
        />

        <h1 className="text-7xl font-bold mb-8">
          <span className="bg-gradient-to-r from-amber-200 via-yellow-500 to-amber-200 text-transparent bg-clip-text">
            Time Portal
          </span>
        </h1>
        
        <p className="text-2xl mb-12 text-slate-300 font-light">
          Journey through time to converse with history's greatest minds
        </p>
        
        <form onSubmit={handleSearch} className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-amber-500/20 via-yellow-500/20 to-amber-500/20 rounded-lg blur group-hover:blur-xl transition-all duration-500"></div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Enter a historical figure's name..."
            className="w-full px-6 py-4 bg-slate-800/50 border border-amber-500/30 rounded-lg text-lg placeholder-slate-400 relative z-10 focus:outline-none focus:border-amber-500 transition-colors"
          />
          <button
            type="submit"
            className="mt-6 px-8 py-3 bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-500 rounded-lg text-black font-semibold hover:from-amber-400 hover:to-yellow-400 transition-all duration-300 hover:scale-105 transform"
          >
            Begin Time Travel
          </button>
        </form>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          {['Leonardo da Vinci', 'Marie Curie', 'Albert Einstein'].map((name, i) => (
            <motion.div
              key={name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              onClick={() => navigate(`/chat/${encodeURIComponent(name)}`)}
              className="p-4 border border-amber-500/30 rounded-lg bg-gradient-to-br from-slate-800/50 to-slate-700/50 cursor-pointer hover:border-amber-500 transition-all duration-300 hover:scale-105 transform group"
            >
              <p className="text-amber-500 group-hover:text-amber-400 transition-colors">{name}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}