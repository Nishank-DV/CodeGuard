import React from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  glow?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, className = '', glow = false, onClick }) => {
  return (
    <motion.div
      className={`
        bg-cyber-surface border border-cyber-border rounded-xl p-6
        backdrop-blur-md transition-all duration-300
        ${glow ? 'shadow-lg shadow-cyan-500/20' : ''}
        ${onClick ? 'cursor-pointer hover:border-cyan-500/50' : ''}
        ${className}
      `}
      whileHover={onClick ? { scale: 1.02 } : {}}
      onClick={onClick}
    >
      {children}
    </motion.div>
  );
};
