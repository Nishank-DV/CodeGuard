import React from 'react';

interface BadgeProps {
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  children: React.ReactNode;
  className?: string;
}

export const SeverityBadge: React.FC<BadgeProps> = ({ severity, children, className = '' }) => {
  const severityStyles = {
    critical: 'bg-red-900 text-red-100 border border-red-700',
    high: 'bg-orange-900 text-orange-100 border border-orange-700',
    medium: 'bg-yellow-900 text-yellow-100 border border-yellow-700',
    low: 'bg-blue-900 text-blue-100 border border-blue-700',
    info: 'bg-cyan-900 text-cyan-100 border border-cyan-700',
  };

  return (
    <span
      className={`
        inline-flex items-center px-3 py-1 rounded-full text-sm font-medium
        ${severityStyles[severity]}
        ${className}
      `}
    >
      {children}
    </span>
  );
};
