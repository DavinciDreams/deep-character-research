import { motion } from 'framer-motion';

export default function LoadingScreen() {
  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center">
      <div className="text-center">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 360],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="w-32 h-32 border-4 border-amber-500 rounded-full mx-auto mb-8 relative"
        >
          <div className="absolute inset-0 border-4 border-yellow-500 rounded-full rotate-45"></div>
          <div className="absolute inset-0 border-4 border-orange-500 rounded-full -rotate-45"></div>
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
          className="text-2xl font-bold text-amber-500"
        >
          Initializing Time Travel
        </motion.h2>
        
        <p className="mt-4 text-slate-400">Establishing temporal connection...</p>
      </div>
    </div>
  );
}