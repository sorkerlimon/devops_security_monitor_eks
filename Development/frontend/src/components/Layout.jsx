import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: '📊', color: '#0ea5e9' },
    { name: 'Network Monitor', href: '/network', icon: '🌐', color: '#22c55e' },
    { name: 'Malware Detector', href: '/malware', icon: '🛡️', color: '#ef4444' },
    { name: 'Web Monitor', href: '/web', icon: '🌍', color: '#f59e0b' },
  ];

  const isCurrentPath = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div style={{ 
      height: '100vh', 
      display: 'flex', 
      overflow: 'hidden', 
      backgroundColor: '#0f172a' 
    }}>
      {/* Desktop sidebar */}
      <div style={{ 
        display: 'none', 
        '@media (min-width: 1024px)': { display: 'flex' },
        flexShrink: 0 
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', width: '16rem' }}>
          <div style={{ 
            display: 'flex', 
            flexDirection: 'column', 
            height: '0', 
            flex: '1', 
            borderRight: '1px solid #374151', 
            backgroundColor: '#1e293b' 
          }}>
            <div style={{ 
              flex: '1', 
              display: 'flex', 
              flexDirection: 'column', 
              paddingTop: '1.25rem', 
              paddingBottom: '1rem', 
              overflowY: 'auto' 
            }}>
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                flexShrink: '0', 
                paddingLeft: '1rem', 
                paddingRight: '1rem' 
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div style={{ 
                    width: '2.5rem', 
                    height: '2.5rem', 
                    background: 'linear-gradient(135deg, #0ea5e9, #0284c7)', 
                    borderRadius: '0.5rem', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center' 
                  }}>
                    <span style={{ fontSize: '1.5rem' }}>🛡️</span>
                  </div>
                  <div>
                    <h1 style={{ fontSize: '1.125rem', fontWeight: 'bold', color: 'white' }}>SECURITY</h1>
                    <p style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace' }}>MONITOR</p>
                  </div>
                </div>
              </div>
              <nav style={{ marginTop: '2rem', flex: '1', paddingLeft: '0.5rem', paddingRight: '0.5rem' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                  {navigation.map((item) => {
                    const isActive = isCurrentPath(item.href);
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          paddingLeft: '0.75rem',
                          paddingRight: '0.75rem',
                          paddingTop: '0.75rem',
                          paddingBottom: '0.75rem',
                          fontSize: '0.875rem',
                          fontWeight: '500',
                          borderRadius: '0.5rem',
                          transition: 'all 0.2s',
                          textDecoration: 'none',
                          backgroundColor: isActive ? `rgba(${item.color === '#0ea5e9' ? '14, 165, 233' : item.color === '#22c55e' ? '34, 197, 94' : item.color === '#ef4444' ? '239, 68, 68' : '245, 158, 11'}, 0.1)` : 'transparent',
                          border: isActive ? `1px solid ${item.color}40` : '1px solid transparent',
                          color: isActive ? item.color : '#9ca3af'
                        }}
                      >
                        <span style={{ marginRight: '0.75rem', fontSize: '1.25rem' }}>{item.icon}</span>
                        {item.name}
                      </Link>
                    );
                  })}
                </div>
              </nav>
            </div>
            <div style={{ 
              flexShrink: '0', 
              display: 'flex', 
              borderTop: '1px solid #374151', 
              padding: '1rem' 
            }}>
              <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                <div style={{ flexShrink: '0' }}>
                  <div style={{ 
                    height: '2.5rem', 
                    width: '2.5rem', 
                    borderRadius: '50%', 
                    background: 'linear-gradient(135deg, #0ea5e9, #0284c7)', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center' 
                  }}>
                    <span style={{ color: 'white', fontSize: '1.25rem' }}>👤</span>
                  </div>
                </div>
                <div style={{ marginLeft: '0.75rem', flex: '1' }}>
                  <p style={{ fontSize: '0.875rem', fontWeight: '500', color: 'white', margin: 0 }}>
                    {user?.full_name || 'User'}
                  </p>
                  <p style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace', margin: 0 }}>
                    {user?.username || 'username'}
                  </p>
                </div>
                <button
                  onClick={logout}
                  style={{
                    flexShrink: '0',
                    backgroundColor: '#374151',
                    padding: '0.5rem',
                    color: '#9ca3af',
                    borderRadius: '0.5rem',
                    border: 'none',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                >
                  <span style={{ fontSize: '1rem' }}>🚪</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div style={{ display: 'flex', flexDirection: 'column', width: '0', flex: '1', overflow: 'hidden' }}>
        {/* Mobile header */}
        <div style={{ 
          display: 'block',
          '@media (min-width: 1024px)': { display: 'none' },
          paddingLeft: '0.25rem',
          paddingTop: '0.25rem'
        }}>
          <button
            type="button"
            style={{
              marginLeft: '-0.125rem',
              marginTop: '-0.125rem',
              height: '3rem',
              width: '3rem',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '0.375rem',
              color: '#9ca3af',
              border: 'none',
              background: 'none',
              cursor: 'pointer'
            }}
            onClick={() => setSidebarOpen(true)}
          >
            <span style={{ fontSize: '1.5rem' }}>☰</span>
          </button>
        </div>

        {/* Status bar */}
        <div style={{ 
          backgroundColor: '#1e293b', 
          borderBottom: '1px solid #374151', 
          paddingLeft: '1rem', 
          paddingRight: '1rem', 
          paddingTop: '0.5rem', 
          paddingBottom: '0.5rem' 
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ 
                  width: '8px', 
                  height: '8px', 
                  backgroundColor: '#22c55e', 
                  borderRadius: '50%', 
                  animation: 'pulse 2s infinite' 
                }}></div>
                <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace' }}>SYSTEM ONLINE</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontSize: '1rem' }}>📊</span>
                <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace' }}>MONITORING ACTIVE</span>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '1rem' }}>⚡</span>
              <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace' }}>
                {new Date().toLocaleTimeString()}
              </span>
            </div>
          </div>
        </div>

        {/* Main content area */}
        <main style={{ 
          flex: '1', 
          position: 'relative', 
          overflowY: 'auto', 
          outline: 'none' 
        }}>
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
