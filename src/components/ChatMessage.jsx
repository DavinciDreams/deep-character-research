import { motion } from 'framer-motion';
import clsx from 'clsx';

export default function ChatMessage({ type, content }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={clsx(
        "max-w-3xl rounded-lg p-4",
        type === 'user' ? 'ml-auto bg-slate-700' : 'bg-gradient-to-r from-amber-500/10 to-yellow-500/10 border border-amber-500/30'
      )}
    >
      <p className={clsx(
        type === 'user' ? 'text-white' : 'text-amber-100'
      )}>
        {content}
      </p>
    </motion.div>
  );
}