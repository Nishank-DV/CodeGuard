import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from './Button';

export const HeroSection: React.FC = () => {
  return (
    <div className="relative overflow-hidden min-h-screen flex items-center justify-center pt-20 pb-12">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-radial from-cyan-500/10 via-transparent to-transparent opacity-20" />
        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl opacity-30" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl opacity-30" />
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <span className="inline-block px-4 py-2 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-cyan-400 text-sm font-medium">
            🚀 Next-Generation Security Scanning
          </span>
        </motion.div>

        {/* Title */}
        <motion.h1
          className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
            Find Vulnerabilities
          </span>
          <br />
          <span className="text-white">Before Your Users Do</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          className="text-lg text-gray-300 mb-8 max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          CodeGuard uses AI-assisted static analysis to detect security vulnerabilities in your code in real-time. 
          Shift-left security with intelligent reasoning about your codebase.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Link to="/analyze">
            <Button variant="primary" size="lg" className="px-10">
              Start Analyzing
            </Button>
          </Link>
          <Link to="/features">
            <Button variant="ghost" size="lg" className="px-10">
              Learn More
            </Button>
          </Link>
        </motion.div>

        {/* Feature highlights */}
        <motion.div
          className="grid md:grid-cols-3 gap-6 mt-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <div className="p-4 bg-cyber-surface/50 border border-cyber-border rounded-lg backdrop-blur-sm">
            <div className="text-2xl mb-2">⚡</div>
            <h3 className="font-semibold text-white mb-1">Real-time Scanning</h3>
            <p className="text-sm text-gray-400">Instant vulnerability detection</p>
          </div>
          <div className="p-4 bg-cyber-surface/50 border border-cyber-border rounded-lg backdrop-blur-sm">
            <div className="text-2xl mb-2">🧠</div>
            <h3 className="font-semibold text-white mb-1">AI-Powered</h3>
            <p className="text-sm text-gray-400">Advanced threat reasoning</p>
          </div>
          <div className="p-4 bg-cyber-surface/50 border border-cyber-border rounded-lg backdrop-blur-sm">
            <div className="text-2xl mb-2">📊</div>
            <h3 className="font-semibold text-white mb-1">Actionable Insights</h3>
            <p className="text-sm text-gray-400">Secure fix recommendations</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
