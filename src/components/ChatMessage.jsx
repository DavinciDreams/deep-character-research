import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

export default function ChatMessage({ type, content }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={clsx(
        "max-w-3xl rounded-lg p-6 backdrop-blur-sm",
        type === 'user' 
          ? 'ml-auto bg-slate-700/90 border border-slate-600'
          : 'bg-gradient-to-r from-amber-500/10 to-yellow-500/10 border border-amber-500/30'
      )}
    >
      <div className="relative">
        {type !== 'user' && (
          <div className="absolute -left-3 -top-3 w-6 h-6 bg-amber-500/20 rounded-full animate-time-pulse"></div>
        )}
        <p className={clsx(
          "prose prose-lg",
          type === 'user' ? 'text-white' : 'text-amber-100'
        )}>
          {content}
        </p>
      </div>
    </motion.div>
  );
}