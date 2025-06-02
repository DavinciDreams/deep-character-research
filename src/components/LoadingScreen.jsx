import React from 'react';
import { motion } from 'framer-motion';

export default function LoadingScreen() {
  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-time-pattern opacity-10"></div>
      
      {/* Animated clockwork background */}
      {[...Array(8)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute border-2 border-amber-500/10 rounded-full"
          style={{
            width: `${100 + i * 50}px`,
            height: `${100 + i * 50}px`,
            top: '50%',
            left: '50%',
            x: '-50%',
            y: '-50%'
          }}
          animate={{
            rotate: 360,
            scale: [1, 1.1, 1]
          }}
          transition={{
            duration: 10 + i * 2,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      ))}
      
      <div className="text-center relative z-10">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 360],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="relative w-40 h-40 mx-auto mb-8"
        >
          {/* Central mechanism */}
          <div className="absolute inset-0 border-4 border-amber-500/30 rounded-full animate-time-spin"></div>
          <div className="absolute inset-2 border-4 border-yellow-500/40 rounded-full animate-time-spin" style={{ animationDirection: 'reverse' }}></div>
          <div className="absolute inset-4 border-4 border-orange-500/50 rounded-full animate-time-spin"></div>
          <div className="absolute inset-[42%] bg-gradient-to-br from-amber-400 to-yellow-500 rounded-full animate-time-pulse shadow-lg shadow-amber-500/20"></div>
        </motion.div>
        
        <motion.h2
          animate={{
            opacity: [0.5, 1, 0.5],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="text-3xl font-bold bg-gradient-to-r from-amber-200 via-yellow-500 to-amber-200 text-transparent bg-clip-text"
        >
          Initializing Time Travel
        </motion.h2>
        
        <div className="mt-8 space-y-2">
          {[
            'Calibrating temporal coordinates...',
            'Stabilizing quantum fluctuations...',
            'Establishing historical connection...'
          ].map((text, i) => (
            <motion.p
              key={text}
              initial={{ opacity: 0 }}
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.3,
                ease: "easeInOut"
              }}
              className="text-slate-400"
            >
              {text}
            </motion.p>
          ))}
        </div>
      </div>
    </div>
  );
}