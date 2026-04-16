import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', ...props }, ref) => (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-cyber-accent mb-2">
          {label}
        </label>
      )}
      <input
        ref={ref}
        className={`
          w-full px-4 py-2.5 bg-cyber-surface border border-cyber-border rounded-lg
          text-white focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20
          transition-all duration-300 placeholder-gray-500
          ${error ? 'border-red-500 focus:ring-red-500/20' : ''}
          ${className}
        `}
        {...props}
      />
      {error && <p className="text-red-400 text-sm mt-1">{error}</p>}
    </div>
  )
);

Input.displayName = 'Input';
