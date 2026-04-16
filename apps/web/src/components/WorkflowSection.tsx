import React from 'react';
import { motion } from 'framer-motion';
import { Card } from './Card';

interface WorkflowStep {
  step: number;
  title: string;
  description: string;
}

interface WorkflowSectionProps {
  steps: WorkflowStep[];
  title?: string;
}

export const WorkflowSection: React.FC<WorkflowSectionProps> = ({ steps, title = 'How CodeGuard Works' }) => {
  return (
    <div className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.h2
          className="text-4xl font-bold mb-12 text-center"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
            {title}
          </span>
        </motion.h2>

        <div className="grid md:grid-cols-4 gap-8 relative">
          {/* Connection lines */}
          <div className="hidden md:block absolute top-1/4 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500/30 to-purple-500/30 -z-10" />

          {steps.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
              viewport={{ once: true, margin: '-100px' }}
            >
              <Card className="relative h-full text-center">
                <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 w-12 h-12 bg-cyber-bg border-4 border-cyber-border rounded-full flex items-center justify-center">
                  <span className="font-bold text-cyan-400">{item.step}</span>
                </div>
                <h3 className="text-xl font-semibold mt-8 mb-3 text-white">
                  {item.title}
                </h3>
                <p className="text-gray-400 text-sm leading-relaxed">
                  {item.description}
                </p>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};
