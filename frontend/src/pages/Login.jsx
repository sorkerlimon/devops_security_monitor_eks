import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(formData.username, formData.password);
    
    if (result.success) {
      // Navigate to dashboard after successful login
      setTimeout(() => {
        navigate('/');
      }, 100);
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

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
      <div style={{ 
        position: 'relative', 
        width: '100%', 
        maxWidth: '28rem', 
        margin: '0 auto', 
        padding: '0 1.5rem' 
      }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            width: '5rem', 
            height: '5rem', 
            background: 'linear-gradient(135deg, #0ea5e9, #0284c7)', 
            borderRadius: '1rem', 
            marginBottom: '1.5rem', 
            boxShadow: '0 25px 50px -12px rgba(14, 165, 233, 0.25)' 
          }}>
            <span style={{ color: 'white', fontSize: '2.5rem' }}>🛡️</span>
          </div>
          <h1 style={{ 
            fontSize: '2.5rem', 
            fontWeight: 'bold', 
            background: 'linear-gradient(135deg, #0ea5e9, #0284c7)', 
            WebkitBackgroundClip: 'text', 
            WebkitTextFillColor: 'transparent', 
            marginBottom: '0.5rem' 
          }}>
            SECURITY MONITOR
          </h1>
          <p style={{ color: '#9ca3af', fontFamily: 'monospace', fontSize: '0.875rem' }}>
            [AUTHENTICATION REQUIRED]
          </p>
        </div>
        
        {/* Login Form */}
        <div style={{ 
          backgroundColor: 'rgba(30, 41, 59, 0.5)', 
          backdropFilter: 'blur(12px)', 
          borderRadius: '0.75rem', 
          border: '1px solid rgba(55, 65, 81, 1)', 
          padding: '2rem', 
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' 
        }}>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {/* Username Field */}
            <div>
              <label htmlFor="username" style={{ 
                display: 'block', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                color: '#d1d5db', 
                marginBottom: '0.5rem' 
              }}>
                USERNAME
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                style={{
                  width: '100%',
                  height: '3rem',
                  padding: '0.75rem 1rem',
                  backgroundColor: 'rgba(55, 65, 81, 0.5)',
                  border: '1px solid #4b5563',
                  borderRadius: '0.5rem',
                  color: 'white',
                  fontSize: '0.875rem'
                }}
                placeholder="Enter username"
                value={formData.username}
                onChange={handleChange}
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" style={{ 
                display: 'block', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                color: '#d1d5db', 
                marginBottom: '0.5rem' 
              }}>
                PASSWORD
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  style={{
                    width: '100%',
                    height: '3rem',
                    padding: '0.75rem 1rem',
                    backgroundColor: 'rgba(55, 65, 81, 0.5)',
                    border: '1px solid #4b5563',
                    borderRadius: '0.5rem',
                    color: 'white',
                    fontSize: '0.875rem'
                  }}
                  placeholder="Enter password"
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  style={{
                    position: 'absolute',
                    right: '1rem',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    color: '#9ca3af',
                    cursor: 'pointer'
                  }}
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? '🙈' : '👁️'}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem', 
                padding: '1rem', 
                backgroundColor: 'rgba(239, 68, 68, 0.1)', 
                border: '1px solid rgba(239, 68, 68, 0.3)', 
                borderRadius: '0.5rem' 
              }}>
                <span style={{ color: '#fca5a5' }}>⚠️</span>
                <span style={{ color: '#fca5a5', fontSize: '0.875rem' }}>{error}</span>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              style={{
                width: '100%',
                height: '3rem',
                background: 'linear-gradient(135deg, #0ea5e9, #0284c7)',
                color: 'white',
                border: 'none',
                borderRadius: '0.5rem',
                fontSize: '1rem',
                fontWeight: '600',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.5 : 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem'
              }}
            >
              {loading ? (
                <>
                  <div style={{ 
                    width: '1.25rem', 
                    height: '1.25rem', 
                    border: '2px solid white', 
                    borderTop: '2px solid transparent', 
                    borderRadius: '50%', 
                    animation: 'spin 1s linear infinite' 
                  }}></div>
                  <span>AUTHENTICATING...</span>
                </>
              ) : (
                'ACCESS SECURE DASHBOARD'
              )}
            </button>

            {/* Register Link */}
            <div style={{ textAlign: 'center' }}>
              <span style={{ color: '#9ca3af', fontSize: '0.875rem' }}>
                New to Security Monitor?{' '}
                <a
                  href="#"
                  style={{ 
                    color: '#0ea5e9', 
                    fontWeight: '500', 
                    textDecoration: 'none' 
                  }}
                >
                  Create Account
                </a>
              </span>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <p style={{ color: '#6b7280', fontSize: '0.75rem', fontFamily: 'monospace' }}>
            © 2024 Security Monitor • Advanced Threat Detection System
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
