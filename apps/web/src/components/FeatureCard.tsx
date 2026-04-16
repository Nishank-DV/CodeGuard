import React from 'react';
import { motion } from 'framer-motion';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  delay?: number;
}

export const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, delay = 0 }) => {
  return (
    <motion.div
      className="p-6 bg-cyber-surface border border-cyber-border rounded-xl backdrop-blur-sm hover:border-cyan-500/50 transition-all duration-300 group cursor-pointer"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
      whileHover={{ y: -5, shadow: '0 10px 30px rgba(0,217,255,0.1)' }}
      viewport={{ once: true, margin: '-100px' }}
    >
      <div className="mb-4 p-3 bg-cyber-surface-dark rounded-lg w-fit group-hover:bg-cyan-500/10 transition-colors">
        <div className="text-cyan-400 group-hover:text-cyan-300 transition-colors">
          {icon}
        </div>
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
    </motion.div>
  );
};
