import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from '@/components';
import { HomePage, FeaturesPage, AboutPage, AnalyzePage, DashboardPage, ScanHistoryPage, LoginPage } from '@/pages';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/features" element={<FeaturesPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/analyze"
          element={
            <ProtectedRoute allowedRoles={["admin", "analyst"]}>
              <AnalyzePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={["admin", "analyst", "viewer"]}>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/history"
          element={
            <ProtectedRoute allowedRoles={["admin", "analyst", "viewer"]}>
              <ScanHistoryPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
