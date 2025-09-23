import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import NetworkMonitor from './pages/NetworkMonitor';
import MalwareDetector from './pages/MalwareDetector';
import WebMonitor from './pages/WebMonitor';
import Layout from './components/Layout';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        backgroundColor: '#0f172a',
        backgroundImage: `
          radial-gradient(circle at 20% 80%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, rgba(34, 197, 94, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 40% 40%, rgba(239, 68, 68, 0.1) 0%, transparent 50%)
        `
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            width: '64px', 
            height: '64px', 
            border: '2px solid #0ea5e9', 
            borderTop: '2px solid transparent', 
            borderRadius: '50%', 
            animation: 'spin 1s linear infinite',
            margin: '0 auto 16px'
          }}></div>
          <div style={{ color: '#0ea5e9', fontFamily: 'monospace' }}>INITIALIZING SECURITY PROTOCOLS...</div>
        </div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
}

function AppRoutes() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/network"
            element={
              <ProtectedRoute>
                <Layout>
                  <NetworkMonitor />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/malware"
            element={
              <ProtectedRoute>
                <Layout>
                  <MalwareDetector />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/web"
            element={
              <ProtectedRoute>
                <Layout>
                  <WebMonitor />
                </Layout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;