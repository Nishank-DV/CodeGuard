import React from 'react';
import { Link } from 'react-router-dom';
import { Code2, Github, Linkedin, Twitter } from 'lucide-react';

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-cyber-surface border-t border-cyber-border mt-20 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <Link to="/" className="flex items-center gap-2 mb-4">
              <Code2 className="w-6 h-6 text-cyan-400" />
              <span className="font-bold text-white">CodeGuard</span>
            </Link>
            <p className="text-gray-400 text-sm">
              AI-assisted static code analysis for modern development.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-semibold text-white mb-4">Product</h3>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><Link to="/features" className="hover:text-cyan-400">Features</Link></li>
              <li><Link to="/analyze" className="hover:text-cyan-400">Analyze Code</Link></li>
              <li><a href="#" className="hover:text-cyan-400">Pricing</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-semibold text-white mb-4">Resources</h3>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><Link to="/about" className="hover:text-cyan-400">About</Link></li>
              <li><a href="#" className="hover:text-cyan-400">Documentation</a></li>
              <li><a href="#" className="hover:text-cyan-400">Blog</a></li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h3 className="font-semibold text-white mb-4">Follow</h3>
            <div className="flex gap-4">
              <a href="#" className="text-gray-400 hover:text-cyan-400 transition">
                <Github size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-cyan-400 transition">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-cyan-400 transition">
                <Linkedin size={20} />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-cyber-border pt-8 flex flex-col md:flex-row justify-between items-center text-gray-400 text-sm">
          <p>&copy; {currentYear} CodeGuard. All rights reserved.</p>
          <div className="flex gap-6 mt-4 md:mt-0">
            <a href="#" className="hover:text-cyan-400">Privacy Policy</a>
            <a href="#" className="hover:text-cyan-400">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
};
