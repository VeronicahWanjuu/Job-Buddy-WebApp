/**
 * Main App Component
 * 
 * This is the root component that sets up routing, authentication context,
 * and the overall layout of the application.
 */

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, Box } from '@mui/material';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';

// Import pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Applications from './pages/Applications';
import Companies from './pages/Companies';
import Profile from './pages/Profile';

// Create custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#667eea',
    },
    secondary: {
      main: '#764ba2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
});

const AppContent = () => {
  const { isAuthenticated } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {isAuthenticated && <Sidebar open={sidebarOpen} />}
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {isAuthenticated && <Navbar />}
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Routes */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />

            {/* Redirect to dashboard by default */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* Protected Routes for Main Features */}
            <Route
              path="/applications"
              element={
                <ProtectedRoute>
                  <Applications />
                </ProtectedRoute>
              }
            />
            <Route
              path="/companies"
              element={
                <ProtectedRoute>
                  <Companies />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />

            {/* Placeholder routes for future pages */}
            <Route
              path="/contacts"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>🤝 Contacts (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/outreach"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>📞 Outreach (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/cv-matcher"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>📄 CV Matcher (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/goals"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>🎯 Goals (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/resources"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>📚 Resources (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/coaches"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>👨‍🏫 Coaches (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/notifications"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>🔔 Notifications (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/onboarding"
              element={
                <ProtectedRoute>
                  <div style={{ padding: '20px' }}>
                    <h1>🚀 Onboarding (Coming Soon)</h1>
                  </div>
                </ProtectedRoute>
              }
            />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
};

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
};

export default App;
