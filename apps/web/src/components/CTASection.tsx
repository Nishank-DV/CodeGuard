import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from './Button';

interface CTASectionProps {
  title: string;
  subtitle: string;
  buttonText?: string;
  buttonLink?: string;
}

export const CTASection: React.FC<CTASectionProps> = ({
  title,
  subtitle,
  buttonText = 'Get Started',
  buttonLink = '/analyze'
}) => {
  return (
    <section className="relative py-20 overflow-hidden">
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-600/20 to-purple-600/20 opacity-30" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl" />
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.h2
          className="text-4xl md:text-5xl font-bold mb-6"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
            {title}
          </span>
        </motion.h2>

        <motion.p
          className="text-lg text-gray-300 mb-8 max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          viewport={{ once: true }}
        >
          {subtitle}
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          viewport={{ once: true }}
        >
          <Link to={buttonLink}>
            <Button variant="primary" size="lg" className="px-10">
              {buttonText}
            </Button>
          </Link>
        </motion.div>
      </div>
    </section>
  );
};
