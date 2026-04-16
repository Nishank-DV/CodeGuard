import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Code2, Menu, X } from 'lucide-react';
import { Button } from './Button';

export const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <motion.nav
      className="sticky top-0 z-50 bg-cyber-bg/80 backdrop-blur-md border-b border-cyber-border"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="p-2 bg-gradient-to-tr from-cyan-500 to-purple-600 rounded-lg group-hover:shadow-lg group-hover:shadow-cyan-500/50 transition-all">
              <Code2 className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              CodeGuard
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <Link to="/features" className="text-gray-300 hover:text-cyan-400 transition">
              Features
            </Link>
            <Link to="/dashboard" className="text-gray-300 hover:text-cyan-400 transition">
              Dashboard
            </Link>
            <Link to="/history" className="text-gray-300 hover:text-cyan-400 transition">
              History
            </Link>
            <Link to="/about" className="text-gray-300 hover:text-cyan-400 transition">
              About
            </Link>
            <Link to="/analyze" className="text-gray-300 hover:text-cyan-400 transition">
              Analyze
            </Link>
          </div>

          {/* CTA Button */}
          <div className="hidden md:flex gap-4">
            <Link to="/analyze">
              <Button variant="primary">Try CodeGuard</Button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-cyan-400"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <motion.div
            className="md:hidden pb-4 border-t border-cyber-border"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Link to="/features" className="block py-2 text-gray-300 hover:text-cyan-400">
              Features
            </Link>
            <Link to="/about" className="block py-2 text-gray-300 hover:text-cyan-400">
              About
            </Link>
            <Link to="/dashboard" className="block py-2 text-gray-300 hover:text-cyan-400">
              Dashboard
            </Link>
            <Link to="/history" className="block py-2 text-gray-300 hover:text-cyan-400">
              History
            </Link>
            <Link to="/analyze" className="block py-2 text-gray-300 hover:text-cyan-400">
              Analyze
            </Link>
            <div className="pt-4">
              <Link to="/analyze" className="w-full">
                <Button variant="primary" className="w-full">
                  Try CodeGuard
                </Button>
              </Link>
            </div>
          </motion.div>
        )}
      </div>
    </motion.nav>
  );
};
