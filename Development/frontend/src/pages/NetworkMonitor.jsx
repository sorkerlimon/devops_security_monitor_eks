import React from 'react';

function NetworkMonitor() {
  return (
    <div style={{ 
      minHeight: '100vh', 
      padding: '2rem',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
      backgroundImage: `
        radial-gradient(circle at 20% 80%, rgba(34, 197, 94, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(34, 197, 94, 0.1) 0%, transparent 50%)
      `
    }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ 
          fontSize: '3rem', 
          fontWeight: 'bold', 
          background: 'linear-gradient(135deg, #22c55e, #16a34a)', 
          WebkitBackgroundClip: 'text', 
          WebkitTextFillColor: 'transparent', 
          marginBottom: '1rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '1rem'
        }}>
          <span style={{ fontSize: '2.5rem' }}>🌐</span>
          NETWORK MONITOR
        </h1>
        <p style={{ color: '#9ca3af', fontFamily: 'monospace', fontSize: '1.125rem' }}>
          [REAL-TIME PORT SCANNING & ANALYSIS]
        </p>
      </div>

      {/* Coming Soon Message */}
      <div style={{ 
        backgroundColor: 'rgba(30, 41, 59, 0.5)', 
        backdropFilter: 'blur(12px)', 
        borderRadius: '0.75rem', 
        border: '1px solid rgba(34, 197, 94, 0.3)', 
        padding: '3rem', 
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🚧</div>
        <h2 style={{ 
          fontSize: '2rem', 
          fontWeight: 'bold', 
          color: 'white', 
          marginBottom: '1rem' 
        }}>
          NETWORK MONITOR
        </h2>
        <p style={{ 
          fontSize: '1.125rem', 
          color: '#9ca3af', 
          marginBottom: '2rem' 
        }}>
          Advanced network monitoring features coming soon!
        </p>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '1rem',
          marginTop: '2rem'
        }}>
          <div style={{ 
            padding: '1rem', 
            backgroundColor: 'rgba(34, 197, 94, 0.1)', 
            borderRadius: '0.5rem', 
            border: '1px solid rgba(34, 197, 94, 0.3)' 
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🔍</div>
            <h3 style={{ color: '#22c55e', fontWeight: '600', marginBottom: '0.25rem' }}>Port Scanning</h3>
            <p style={{ fontSize: '0.875rem', color: '#9ca3af' }}>Real-time port analysis</p>
          </div>
          <div style={{ 
            padding: '1rem', 
            backgroundColor: 'rgba(34, 197, 94, 0.1)', 
            borderRadius: '0.5rem', 
            border: '1px solid rgba(34, 197, 94, 0.3)' 
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📊</div>
            <h3 style={{ color: '#22c55e', fontWeight: '600', marginBottom: '0.25rem' }}>Network Stats</h3>
            <p style={{ fontSize: '0.875rem', color: '#9ca3af' }}>Comprehensive analytics</p>
          </div>
          <div style={{ 
            padding: '1rem', 
            backgroundColor: 'rgba(34, 197, 94, 0.1)', 
            borderRadius: '0.5rem', 
            border: '1px solid rgba(34, 197, 94, 0.3)' 
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>⚠️</div>
            <h3 style={{ color: '#22c55e', fontWeight: '600', marginBottom: '0.25rem' }}>Alerts</h3>
            <p style={{ fontSize: '0.875rem', color: '#9ca3af' }}>Security notifications</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NetworkMonitor;
