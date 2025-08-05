import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

export default function ChatMessage({ type, content }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={clsx(
        "max-w-3xl rounded-lg p-6 backdrop-blur-sm relative group",
        type === 'user' 
          ? 'ml-auto bg-slate-700/90 border border-slate-600'
          : 'bg-gradient-to-r from-amber-500/10 to-yellow-500/10 border border-amber-500/30'
      )}
    >
      {/* Decorative elements */}
      <div className={clsx(
        "absolute inset-px rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300",
        type === 'user'
          ? 'bg-gradient-to-r from-slate-600/20 to-slate-500/20'
          : 'bg-gradient-to-r from-amber-500/5 to-yellow-500/5'
      )}></div>
      
      {type !== 'user' && (
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.5, 0.2]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute -left-3 -top-3 w-6 h-6 bg-amber-500/20 rounded-full"
        />
      )}
      
      <div className="relative">
        <p className={clsx(
          "prose prose-lg",
          type === 'user' ? 'text-white' : 'text-amber-100'
        )}>
          {content}
        </p>
      </div>
      
      {/* Time travel effect */}
      <div className={clsx(
        "absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none",
        type === 'user'
          ? 'from-slate-400/0 via-slate-400/5 to-slate-400/0'
          : 'from-amber-500/0 via-amber-500/5 to-amber-500/0'
      )}></div>
    </motion.div>
  );
}