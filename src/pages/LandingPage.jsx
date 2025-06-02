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
      
      {/* Animated clockwork elements */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(6)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-40 h-40 border-2 border-amber-500/10 rounded-full"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              scale: 0.5 + Math.random() * 1.5
            }}
            animate={{
              rotate: [0, 360],
              opacity: [0.1, 0.3, 0.1]
            }}
            transition={{
              duration: 20 + Math.random() * 10,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        ))}
      </div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-2xl w-full text-center relative z-10"
      >
        <h1 className="text-7xl font-bold mb-8 relative">
          <span className="absolute -inset-x-20 top-1/2 h-px bg-gradient-to-r from-transparent via-amber-500/50 to-transparent"></span>
          <span className="relative bg-gradient-to-r from-amber-200 via-yellow-500 to-amber-200 text-transparent bg-clip-text">
            Time Portal
          </span>
        </h1>
        
        <p className="text-2xl mb-12 text-slate-300 font-light">
          Journey through time to converse with history's greatest minds
        </p>
        
        <form onSubmit={handleSearch} className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-amber-500 to-yellow-500 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Enter a historical figure's name..."
            className="w-full px-6 py-4 bg-slate-800/50 border border-amber-500/30 rounded-lg text-lg placeholder-slate-400 relative z-10 focus:outline-none focus:border-amber-500 transition-all duration-300"
          />
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="mt-6 px-8 py-3 bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-500 rounded-lg text-black font-semibold relative z-10 overflow-hidden group"
          >
            <span className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></span>
            <span className="relative">Begin Time Travel</span>
          </motion.button>
        </form>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          {['Leonardo da Vinci', 'Marie Curie', 'Albert Einstein'].map((name, i) => (
            <motion.div
              key={name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
              onClick={() => navigate(`/chat/${encodeURIComponent(name)}`)}
              className="p-4 border border-amber-500/30 rounded-lg bg-gradient-to-br from-slate-800/50 to-slate-700/50 cursor-pointer hover:border-amber-500 transition-all duration-300 relative group"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-amber-500/0 via-amber-500/10 to-amber-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <p className="text-amber-500 group-hover:text-amber-400 transition-colors relative z-10">{name}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}