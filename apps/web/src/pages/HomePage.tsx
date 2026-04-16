import React from 'react';
import { motion } from 'framer-motion';
import { Navbar, Footer, HeroSection, FeatureCard, WorkflowSection, CTASection } from '@/components';
import { Zap, Brain, AlertCircle, Shield, Code, BarChart3 } from 'lucide-react';

export const HomePage: React.FC = () => {
  const features = [
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Real-Time Detection',
      description: 'Scan code as you write it. Instant vulnerability detection integrated into your workflow.'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'AI-Powered Analysis',
      description: 'Leverage advanced machine learning to understand code semantics and threat patterns.'
    },
    {
      icon: <AlertCircle className="w-8 h-8" />,
      title: 'OWASP Aligned',
      description: 'Severity classification based on industry standards and best practices.'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Secure Fixes',
      description: 'Get AI-assisted recommendations for safe and effective vulnerability remediation.'
    },
    {
      icon: <Code className="w-8 h-8" />,
      title: 'Multi-Language',
      description: 'Support for Python, JavaScript, Java, C++, Go, and more.'
    },
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: 'Actionable Reports',
      description: 'Comprehensive dashboards with metrics and insights for your security posture.'
    },
  ];

  const workflowSteps = [
    {
      step: 1,
      title: 'Submit Code',
      description: 'Paste or upload your source code to CodeGuard'
    },
    {
      step: 2,
      title: 'AST Analysis',
      description: 'Abstract Syntax Tree parsing and structural analysis'
    },
    {
      step: 3,
      title: 'AI Reasoning',
      description: 'Deep semantic analysis with AI threat detection'
    },
    {
      step: 4,
      title: 'Get Insights',
      description: 'Receive detailed reports with fix recommendations'
    },
  ];

  return (
    <div className="bg-cyber-bg text-white">
      <Navbar />
      <HeroSection />

      {/* Why CodeGuard Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            className="mb-16 text-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">
              <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                Why CodeGuard?
              </span>
            </h2>
            <p className="text-gray-300 max-w-2xl mx-auto">
              Security vulnerabilities cost time and money. Shift-left with CodeGuard to catch issues before they reach production.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div
              className="p-8 bg-cyber-surface border border-cyber-border rounded-xl"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ delay: 0 }}
              viewport={{ once: true }}
            >
              <div className="text-3xl mb-4">⏱️</div>
              <h3 className="text-xl font-semibold mb-2">Save Time</h3>
              <p className="text-gray-400">
                Automated scanning eliminates manual code reviews and reduces security overhead.
              </p>
            </motion.div>

            <motion.div
              className="p-8 bg-cyber-surface border border-cyber-border rounded-xl"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              viewport={{ once: true }}
            >
              <div className="text-3xl mb-4">🛡️</div>
              <h3 className="text-xl font-semibold mb-2">Reduce Risk</h3>
              <p className="text-gray-400">
                Catch vulnerabilities early in the development cycle before they become costly production issues.
              </p>
            </motion.div>

            <motion.div
              className="p-8 bg-cyber-surface border border-cyber-border rounded-xl"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              viewport={{ once: true }}
            >
              <div className="text-3xl mb-4">🚀</div>
              <h3 className="text-xl font-semibold mb-2">Faster Releases</h3>
              <p className="text-gray-400">
                Improve developer velocity with confidence through continuous, automated security scanning.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 border-y border-cyber-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.h2
            className="text-4xl font-bold mb-12 text-center"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Powerful Features
            </span>
          </motion.h2>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard
                key={index}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                delay={index * 0.1}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <WorkflowSection steps={workflowSteps} />

      {/* CTA Section */}
      <CTASection
        title="Ready to Secure Your Code?"
        subtitle="Join developers who are shifting left on security with CodeGuard. Start your free analysis now."
        buttonText="Start Analyzing"
        buttonLink="/analyze"
      />

      <Footer />
    </div>
  );
};
