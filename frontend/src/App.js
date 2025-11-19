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
            {/* Main Dashboard - No Authentication Required */}
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* Main Features - No Authentication Required */}
            <Route path="/applications" element={<Applications />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/profile" element={<Profile />} />

            {/* Placeholder routes for future pages */}
            <Route path="/contacts" element={<div style={{ padding: '20px' }}><h1>🤝 Contacts (Coming Soon)</h1></div>} />
            <Route path="/outreach" element={<div style={{ padding: '20px' }}><h1>📞 Outreach (Coming Soon)</h1></div>} />
            <Route path="/cv-matcher" element={<div style={{ padding: '20px' }}><h1>📄 CV Matcher (Coming Soon)</h1></div>} />
            <Route path="/goals" element={<div style={{ padding: '20px' }}><h1>🎯 Goals (Coming Soon)</h1></div>} />
            <Route path="/resources" element={<div style={{ padding: '20px' }}><h1>📚 Resources (Coming Soon)</h1></div>} />
            <Route path="/coaches" element={<div style={{ padding: '20px' }}><h1>👨‍🏫 Coaches (Coming Soon)</h1></div>} />
            <Route path="/notifications" element={<div style={{ padding: '20px' }}><h1>🔔 Notifications (Coming Soon)</h1></div>} />
            <Route path="/onboarding" element={<div style={{ padding: '20px' }}><h1>🚀 Onboarding (Coming Soon)</h1></div>} />
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
