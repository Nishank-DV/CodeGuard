import React from 'react';
import { Navigate } from 'react-router-dom';

import { getRole, isAuthenticated } from '@/utils/auth';

interface ProtectedRouteProps {
  children: React.ReactElement;
  allowedRoles?: Array<'admin' | 'analyst' | 'viewer'>;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  const role = getRole();
  if (allowedRoles && role && !allowedRoles.includes(role)) {
    return <Navigate to="/login" replace />;
  }

  return children;
};
