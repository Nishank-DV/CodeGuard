import React from 'react';
import { motion } from 'framer-motion';
import { Navbar, Footer, PageLayout, FeatureCard, CTASection } from '@/components';
import {
  Zap,
  Brain,
  AlertCircle,
  Shield,
  Code,
  BarChart3,
  Filter,
  Eye,
  GitBranch,
  Lock
} from 'lucide-react';

export const FeaturesPage: React.FC = () => {
  const mainFeatures = [
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Real-Time Vulnerability Detection',
      description: 'Scan your code instantly. CodeGuard detects vulnerabilities as you write, providing immediate feedback in your development workflow.'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'AST-Based Structural Analysis',
      description: 'Advanced Abstract Syntax Tree parsing understands code structure deeply, not just pattern matching on surface-level patterns.'
    },
    {
      icon: <AlertCircle className="w-8 h-8" />,
      title: 'AI-Powered Reasoning',
      description: 'Machine learning models reason about vulnerability context, data flow, and semantic meaning of your code.'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'OWASP Severity Classification',
      description: 'Vulnerabilities classified by industry-standard OWASP severity levels: Critical, High, Medium, Low, and Info.'
    },
    {
      icon: <Code className="w-8 h-8" />,
      title: 'Secure Fix Generation',
      description: 'AI-guided secure fix recommendations that show you exactly how to remediate vulnerabilities safely.'
    },
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: 'Comprehensive Dashboards',
      description: 'Interactive reporting dashboards track security metrics, trends, and remediation progress over time.'
    },
    {
      icon: <Filter className="w-8 h-8" />,
      title: 'Customizable Policies',
      description: 'Define custom security policies and rules aligned with your organization\'s standards.'
    },
    {
      icon: <Eye className="w-8 h-8" />,
      title: 'Multi-Language Support',
      description: 'Analyze Python, JavaScript/TypeScript, Java, C++, Go, Rust, and more languages.'
    },
    {
      icon: <GitBranch className="w-8 h-8" />,
      title: 'CI/CD Integration',
      description: 'Seamless integration with your GitHub, GitLab, and Bitbucket workflows. (Phase 2)'
    },
    {
      icon: <Lock className="w-8 h-8" />,
      title: 'Team Collaboration',
      description: 'Invite team members, assign issues, track remediation progress, and collaborate securely.'
    },
  ];

  return (
    <div className="bg-cyber-bg text-white">
      <Navbar />
      <PageLayout
        title="Features"
        subtitle="Comprehensive security scanning powered by AI and advanced static analysis"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
            {mainFeatures.map((feature, index) => (
              <FeatureCard
                key={index}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                delay={index * 0.05}
              />
            ))}
          </div>

          {/* Detailed Feature Sections */}
          <div className="space-y-20">
            {/* Analysis Engine */}
            <motion.div
              className="border-t border-cyber-border pt-20"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <div className="grid md:grid-cols-2 gap-12 items-center">
                <div>
                  <h3 className="text-3xl font-bold mb-6">Advanced Analysis Engine</h3>
                  <p className="text-gray-300 mb-4">
                    CodeGuard combines three powerful analysis techniques:
                  </p>
                  <ul className="space-y-3 text-gray-400">
                    <li className="flex gap-3">
                      <span className="text-cyan-400 font-bold">1.</span>
                      <span><strong>Abstract Syntax Tree (AST)</strong> parsing for structural code analysis</span>
                    </li>
                    <li className="flex gap-3">
                      <span className="text-cyan-400 font-bold">2.</span>
                      <span><strong>Data Flow Analysis</strong> to track sensitive data through your codebase</span>
                    </li>
                    <li className="flex gap-3">
                      <span className="text-cyan-400 font-bold">3.</span>
                      <span><strong>Machine Learning</strong> models for semantic threat detection</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-cyber-surface border border-cyber-border rounded-xl p-8 h-64 flex items-center justify-center text-center">
                  <div>
                    <div className="text-4xl mb-4">📊</div>
                    <p className="text-gray-400">Advanced Analysis Visualization</p>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Severity Classification */}
            <motion.div
              className="border-t border-cyber-border pt-20"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h3 className="text-3xl font-bold mb-8">OWASP-Aligned Severity Classification</h3>
              <div className="grid md:grid-cols-5 gap-4">
                {[
                  { level: 'CRITICAL', color: 'bg-red-900', icon: '🔴' },
                  { level: 'HIGH', color: 'bg-orange-900', icon: '🟠' },
                  { level: 'MEDIUM', color: 'bg-yellow-900', icon: '🟡' },
                  { level: 'LOW', color: 'bg-blue-900', icon: '🔵' },
                  { level: 'INFO', color: 'bg-cyan-900', icon: '🔷' },
                ].map((item, index) => (
                  <motion.div
                    key={index}
                    className={`${item.color} p-6 rounded-lg text-center`}
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    viewport={{ once: true }}
                  >
                    <div className="text-3xl mb-2">{item.icon}</div>
                    <p className="font-semibold">{item.level}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Supported Languages */}
            <motion.div
              className="border-t border-cyber-border pt-20"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h3 className="text-3xl font-bold mb-8">Multi-Language Support</h3>
              <div className="grid md:grid-cols-4 gap-4">
                {['Python', 'JavaScript/TypeScript', 'Java', 'C++', 'Go', 'Rust', 'PHP', 'Ruby'].map((lang, index) => (
                  <div
                    key={index}
                    className="p-4 bg-cyber-surface border border-cyber-border rounded-lg text-center hover:border-cyan-500 transition"
                  >
                    <p className="font-semibold text-white">{lang}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </PageLayout>

      <CTASection
        title="Start Securing Your Code Today"
        subtitle="Experience the power of AI-assisted security analysis. No credit card required."
        buttonText="Try CodeGuard Free"
        buttonLink="/analyze"
      />

      <Footer />
    </div>
  );
};
