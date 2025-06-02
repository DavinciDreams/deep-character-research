import React from 'react';
import { motion } from 'framer-motion';

export default function LoadingScreen() {
  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-time-pattern opacity-10"></div>
      
      <div className="text-center relative z-10">
        <div className="relative">
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
            className="w-40 h-40 mx-auto mb-8"
          >
            {/* Nested rotating circles */}
            <div className="absolute inset-0 border-4 border-amber-500/30 rounded-full animate-time-spin"></div>
            <div className="absolute inset-2 border-4 border-yellow-500/40 rounded-full animate-time-spin" style={{ animationDirection: 'reverse' }}></div>
            <div className="absolute inset-4 border-4 border-orange-500/50 rounded-full animate-time-spin"></div>
            
            {/* Center point */}
            <div className="absolute inset-[42%] bg-amber-500 rounded-full animate-time-pulse"></div>
          </motion.div>
        </div>
        
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
        
        <div className="mt-8 space-y-2 text-slate-400">
          <p className="animate-pulse">Calibrating temporal coordinates...</p>
          <p className="animate-pulse" style={{ animationDelay: '0.2s' }}>Stabilizing quantum fluctuations...</p>
          <p className="animate-pulse" style={{ animationDelay: '0.4s' }}>Establishing historical connection...</p>
        </div>
      </div>
    </div>
  );
}