import React from 'react';
import { motion } from 'framer-motion';
import { Navbar, Footer, PageLayout, Card, CTASection } from '@/components';
import { TrendingUp, Shield, Zap, Users } from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="bg-cyber-bg text-white">
      <Navbar />
      <PageLayout
        title="About CodeGuard"
        subtitle="Building the future of secure software development"
      >
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Problem Statement */}
          <motion.section
            className="mb-20"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold mb-8">The Problem</h2>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 mb-4 text-lg leading-relaxed">
                Security vulnerabilities are one of the leading causes of data breaches and system compromises. 
                Traditional security practices focus on detection after code is deployed (shift-right), but by then, 
                vulnerabilities are already in production affecting real users.
              </p>
              <p className="text-gray-300 mb-4 text-lg leading-relaxed">
                Modern development teams need to <strong>shift-left</strong> — catching vulnerabilities during 
                development, not after deployment. However, existing static analysis tools fall short:
              </p>
              <ul className="space-y-3 text-gray-300">
                <li className="flex gap-3">
                  <span className="text-cyan-400">❌</span>
                  <span>Traditional tools produce excessive false positives, creating alert fatigue</span>
                </li>
                <li className="flex gap-3">
                  <span className="text-cyan-400">❌</span>
                  <span>Pattern-based matching misses context-specific vulnerabilities</span>
                </li>
                <li className="flex gap-3">
                  <span className="text-cyan-400">❌</span>
                  <span>Slow scanning times disrupt developer workflows</span>
                </li>
                <li className="flex gap-3">
                  <span className="text-cyan-400">❌</span>
                  <span>Limited guidance on how to actually fix vulnerabilities</span>
                </li>
              </ul>
            </div>
          </motion.section>

          {/* Solution */}
          <motion.section
            className="border-t border-cyber-border pt-20 mb-20"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold mb-8">The Solution: CodeGuard</h2>
            <p className="text-gray-300 mb-8 text-lg leading-relaxed">
              CodeGuard reimagines static code analysis by combining three powerful techniques:
            </p>

            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <Card glow>
                <div className="text-cyan-400 mb-4">
                  <TrendingUp className="w-10 h-10" />
                </div>
                <h3 className="text-xl font-semibold mb-3">AI-Powered Reasoning</h3>
                <p className="text-gray-400">
                  Machine learning models understand code semantics and context, not just patterns.
                </p>
              </Card>

              <Card glow>
                <div className="text-purple-400 mb-4">
                  <Shield className="w-10 h-10" />
                </div>
                <h3 className="text-xl font-semibold mb-3">AST Analysis</h3>
                <p className="text-gray-400">
                  Deep structural analysis through Abstract Syntax Tree parsing for precision.
                </p>
              </Card>

              <Card glow>
                <div className="text-cyan-300 mb-4">
                  <Zap className="w-10 h-10" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Developer-First Design</h3>
                <p className="text-gray-400">
                  Fast, actionable insights that fit into your existing development workflow.
                </p>
              </Card>
            </div>
          </motion.section>

          {/* Mission & Values */}
          <motion.section
            className="border-t border-cyber-border pt-20 mb-20"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold mb-12">Our Mission & Values</h2>

            <div className="grid md:grid-cols-2 gap-8">
              <motion.div
                className="p-8 bg-cyber-surface border border-cyan-500/30 rounded-xl"
                whileHover={{ y: -5 }}
              >
                <Users className="w-8 h-8 text-cyan-400 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Developer-Centric</h3>
                <p className="text-gray-400">
                  We build tools for developers, by developers. Security shouldn't slow you down—it should 
                  enable you to ship with confidence.
                </p>
              </motion.div>

              <motion.div
                className="p-8 bg-cyber-surface border border-purple-500/30 rounded-xl"
                whileHover={{ y: -5 }}
              >
                <Shield className="w-8 h-8 text-purple-400 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Shift-Left Security</h3>
                <p className="text-gray-400">
                  Catch vulnerabilities early in development where they're cheaper and faster to fix. 
                  We move security from gatekeeping to enablement.
                </p>
              </motion.div>

              <motion.div
                className="p-8 bg-cyber-surface border border-cyan-500/30 rounded-xl"
                whileHover={{ y: -5 }}
              >
                <Zap className="w-8 h-8 text-cyan-400 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Accuracy Over Noise</h3>
                <p className="text-gray-400">
                  Fewer, higher-quality findings mean developers can focus on real threats instead of 
                  chasing false positives.
                </p>
              </motion.div>

              <motion.div
                className="p-8 bg-cyber-surface border border-purple-500/30 rounded-xl"
                whileHover={{ y: -5 }}
              >
                <TrendingUp className="w-8 h-8 text-purple-400 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Continuous Innovation</h3>
                <p className="text-gray-400">
                  We continuously improve our models and add new capabilities based on the latest 
                  security research and industry trends.
                </p>
              </motion.div>
            </div>
          </motion.section>

          {/* Future Vision */}
          <motion.section
            className="border-t border-cyber-border pt-20"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold mb-8">The Road Ahead</h2>
            <div className="bg-gradient-to-r from-cyan-900/20 to-purple-900/20 border border-cyber-border rounded-xl p-8">
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-semibold mb-4">Phase 1: Core Platform</h3>
                  <ul className="space-y-2 text-gray-400">
                    <li>✓ Web-based code analysis</li>
                    <li>✓ Real-time scanning</li>
                    <li>✓ Multi-language support</li>
                    <li>✓ Severity classification</li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-4">Phase 2 & Beyond</h3>
                  <ul className="space-y-2 text-gray-400">
                    <li>🚀 CI/CD integrations</li>
                    <li>🚀 IDE plugins</li>
                    <li>🚀 Team collaboration features</li>
                    <li>🚀 Advanced policies & compliance</li>
                  </ul>
                </div>
              </div>
            </div>
          </motion.section>
        </div>
      </PageLayout>

      <CTASection
        title="Join the Security Revolution"
        subtitle="Start building more secure applications today with CodeGuard."
        buttonText="Start Analyzing"
        buttonLink="/analyze"
      />

      <Footer />
    </div>
  );
};
