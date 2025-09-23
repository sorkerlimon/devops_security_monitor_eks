import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { networkAPI, malwareAPI, webAPI } from '../services/api';

function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    network: { total_scans: 0, open_ports: 0, closed_ports: 0 },
    malware: { total_reports: 0, malware_detected: 0, high_risk_files: 0 },
    web: { total_visits: 0, blocked_visits: 0, suspicious_visits: 0 }
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [networkStats, malwareStats, webStats] = await Promise.all([
        networkAPI.getStats(7), // Last 7 days
        malwareAPI.getStats(7),
        webAPI.getStats(7)
      ]);

      setStats({
        network: networkStats.data,
        malware: malwareStats.data,
        web: webStats.data
      });

      // Fetch recent activity
      const [malwareActivity, webActivity] = await Promise.all([
        malwareAPI.getRecentActivity(5),
        webAPI.getRecentActivity(5)
      ]);

      const activity = [
        ...malwareActivity.data.map(report => ({
          ...report,
          type: 'malware',
          icon: '🛡️',
          color: 'danger',
          message: `Suspicious file: ${report.file_name}`,
          timestamp: report.created_at
        })),
        ...webActivity.data.map(report => ({
          ...report,
          type: 'web',
          icon: '🌍',
          color: 'warning',
          message: `Web activity: ${report.domain}`,
          timestamp: report.created_at
        }))
      ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 10);

      setRecentActivity(activity);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

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
            width: '4rem', 
            height: '4rem', 
            border: '2px solid #0ea5e9', 
            borderTop: '2px solid transparent', 
            borderRadius: '50%', 
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }}></div>
          <div style={{ color: '#0ea5e9', fontFamily: 'monospace', fontSize: '1.125rem' }}>LOADING SECURITY DATA...</div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      padding: '2rem',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
      backgroundImage: `
        radial-gradient(circle at 20% 80%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(34, 197, 94, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(239, 68, 68, 0.1) 0%, transparent 50%)
      `
    }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ 
          fontSize: '3rem', 
          fontWeight: 'bold', 
          background: 'linear-gradient(135deg, #0ea5e9, #0284c7)', 
          WebkitBackgroundClip: 'text', 
          WebkitTextFillColor: 'transparent', 
          marginBottom: '1rem' 
        }}>
          SECURITY DASHBOARD
        </h1>
        <p style={{ color: '#9ca3af', fontFamily: 'monospace', fontSize: '1.125rem' }}>
          [REAL-TIME THREAT MONITORING SYSTEM]
        </p>
        <p style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.5rem' }}>
          Welcome back, {user?.full_name || user?.username}!
        </p>
      </div>

      {/* Stats Grid */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '1.5rem', 
        marginBottom: '3rem' 
      }}>
        {/* Network Monitoring Card */}
        <div style={{ 
          backgroundColor: 'rgba(30, 41, 59, 0.5)', 
          backdropFilter: 'blur(12px)', 
          borderRadius: '0.75rem', 
          border: '1px solid rgba(34, 197, 94, 0.3)', 
          padding: '1.5rem', 
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          transition: 'transform 0.2s ease-in-out'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ 
              padding: '0.75rem', 
              borderRadius: '0.5rem', 
              backgroundColor: 'rgba(34, 197, 94, 0.1)', 
              border: '1px solid rgba(34, 197, 94, 0.3)' 
            }}>
              <span style={{ fontSize: '1.5rem' }}>🌐</span>
            </div>
            <div style={{ 
              width: '12px', 
              height: '12px', 
              backgroundColor: '#22c55e', 
              borderRadius: '50%', 
              animation: 'pulse 2s infinite' 
            }}></div>
          </div>
          <div>
            <h3 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#9ca3af', marginBottom: '0.25rem' }}>
              NETWORK MONITORING
            </h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white', margin: 0 }}>{stats.network.total_scans || 0}</p>
            <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.5rem' }}>
              {stats.network.open_ports || 0} open ports, {stats.network.closed_ports || 0} closed
            </p>
          </div>
        </div>

        {/* Malware Detection Card */}
        <div style={{ 
          backgroundColor: 'rgba(30, 41, 59, 0.5)', 
          backdropFilter: 'blur(12px)', 
          borderRadius: '0.75rem', 
          border: '1px solid rgba(239, 68, 68, 0.3)', 
          padding: '1.5rem', 
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          transition: 'transform 0.2s ease-in-out'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ 
              padding: '0.75rem', 
              borderRadius: '0.5rem', 
              backgroundColor: 'rgba(239, 68, 68, 0.1)', 
              border: '1px solid rgba(239, 68, 68, 0.3)' 
            }}>
              <span style={{ fontSize: '1.5rem' }}>🛡️</span>
            </div>
            <div style={{ 
              width: '12px', 
              height: '12px', 
              backgroundColor: '#ef4444', 
              borderRadius: '50%', 
              animation: 'pulse 2s infinite' 
            }}></div>
          </div>
          <div>
            <h3 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#9ca3af', marginBottom: '0.25rem' }}>
              MALWARE DETECTION
            </h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white', margin: 0 }}>{stats.malware.total_reports || 0}</p>
            <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.5rem' }}>
              {stats.malware.malware_detected || 0} threats, {stats.malware.high_risk_files || 0} high risk
            </p>
          </div>
        </div>

        {/* Web Monitoring Card */}
        <div style={{ 
          backgroundColor: 'rgba(30, 41, 59, 0.5)', 
          backdropFilter: 'blur(12px)', 
          borderRadius: '0.75rem', 
          border: '1px solid rgba(245, 158, 11, 0.3)', 
          padding: '1.5rem', 
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          transition: 'transform 0.2s ease-in-out'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ 
              padding: '0.75rem', 
              borderRadius: '0.5rem', 
              backgroundColor: 'rgba(245, 158, 11, 0.1)', 
              border: '1px solid rgba(245, 158, 11, 0.3)' 
            }}>
              <span style={{ fontSize: '1.5rem' }}>🌍</span>
            </div>
            <div style={{ 
              width: '12px', 
              height: '12px', 
              backgroundColor: '#f59e0b', 
              borderRadius: '50%', 
              animation: 'pulse 2s infinite' 
            }}></div>
          </div>
          <div>
            <h3 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#9ca3af', marginBottom: '0.25rem' }}>
              WEB MONITORING
            </h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white', margin: 0 }}>{stats.web.total_visits || 0}</p>
            <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.5rem' }}>
              {stats.web.blocked_visits || 0} blocked, {stats.web.suspicious_visits || 0} suspicious
            </p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{ 
        backgroundColor: 'rgba(30, 41, 59, 0.5)', 
        backdropFilter: 'blur(12px)', 
        borderRadius: '0.75rem', 
        border: '1px solid rgba(55, 65, 81, 1)', 
        padding: '2rem', 
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        marginBottom: '3rem'
      }}>
        <h3 style={{ 
          fontSize: '1.5rem', 
          fontWeight: 'bold', 
          color: 'white', 
          marginBottom: '1.5rem', 
          display: 'flex', 
          alignItems: 'center' 
        }}>
          <span style={{ marginRight: '0.75rem' }}>⚡</span>
          QUICK ACTIONS
        </h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '1rem' 
        }}>
          <div style={{ 
            padding: '1.5rem', 
            background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05))', 
            border: '1px solid rgba(34, 197, 94, 0.3)', 
            borderRadius: '0.75rem', 
            cursor: 'pointer',
            transition: 'all 0.2s ease-in-out'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span style={{ fontSize: '2rem' }}>🌐</span>
              <div>
                <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: 'white', margin: 0 }}>Network Monitor</h4>
                <p style={{ fontSize: '0.875rem', color: '#9ca3af', margin: 0 }}>Port scanning & analysis</p>
              </div>
            </div>
          </div>
          <div style={{ 
            padding: '1.5rem', 
            background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05))', 
            border: '1px solid rgba(239, 68, 68, 0.3)', 
            borderRadius: '0.75rem', 
            cursor: 'pointer',
            transition: 'all 0.2s ease-in-out'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span style={{ fontSize: '2rem' }}>🛡️</span>
              <div>
                <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: 'white', margin: 0 }}>Malware Detector</h4>
                <p style={{ fontSize: '0.875rem', color: '#9ca3af', margin: 0 }}>File scanning & threats</p>
              </div>
            </div>
          </div>
          <div style={{ 
            padding: '1.5rem', 
            background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05))', 
            border: '1px solid rgba(245, 158, 11, 0.3)', 
            borderRadius: '0.75rem', 
            cursor: 'pointer',
            transition: 'all 0.2s ease-in-out'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span style={{ fontSize: '2rem' }}>🌍</span>
              <div>
                <h4 style={{ fontSize: '1.125rem', fontWeight: '600', color: 'white', margin: 0 }}>Web Monitor</h4>
                <p style={{ fontSize: '0.875rem', color: '#9ca3af', margin: 0 }}>Web activity & filtering</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '1.5rem' 
      }}>
        <div style={{ 
          backgroundColor: 'rgba(30, 41, 59, 0.5)', 
          backdropFilter: 'blur(12px)', 
          borderRadius: '0.75rem', 
          border: '1px solid rgba(55, 65, 81, 1)', 
          padding: '1.5rem', 
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' 
        }}>
          <h3 style={{ 
            fontSize: '1.25rem', 
            fontWeight: 'bold', 
            color: 'white', 
            marginBottom: '1rem', 
            display: 'flex', 
            alignItems: 'center' 
          }}>
            <span style={{ marginRight: '0.75rem' }}>📊</span>
            SYSTEM STATUS
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between', 
              padding: '0.75rem', 
              backgroundColor: 'rgba(34, 197, 94, 0.1)', 
              borderRadius: '0.5rem', 
              border: '1px solid rgba(34, 197, 94, 0.3)' 
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ 
                  width: '12px', 
                  height: '12px', 
                  backgroundColor: '#22c55e', 
                  borderRadius: '50%', 
                  animation: 'pulse 2s infinite' 
                }}></div>
                <span style={{ color: '#22c55e', fontWeight: '500' }}>Network Scanner</span>
              </div>
              <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace' }}>ONLINE</span>
            </div>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between', 
              padding: '0.75rem', 
              backgroundColor: 'rgba(34, 197, 94, 0.1)', 
              borderRadius: '0.5rem', 
              border: '1px solid rgba(34, 197, 94, 0.3)' 
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ 
                  width: '12px', 
                  height: '12px', 
                  backgroundColor: '#22c55e', 
                  borderRadius: '50%', 
                  animation: 'pulse 2s infinite' 
                }}></div>
                <span style={{ color: '#22c55e', fontWeight: '500' }}>Malware Engine</span>
              </div>
              <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace' }}>ONLINE</span>
            </div>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between', 
              padding: '0.75rem', 
              backgroundColor: 'rgba(34, 197, 94, 0.1)', 
              borderRadius: '0.5rem', 
              border: '1px solid rgba(34, 197, 94, 0.3)' 
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ 
                  width: '12px', 
                  height: '12px', 
                  backgroundColor: '#22c55e', 
                  borderRadius: '50%', 
                  animation: 'pulse 2s infinite' 
                }}></div>
                <span style={{ color: '#22c55e', fontWeight: '500' }}>Web Monitor</span>
              </div>
              <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace' }}>ONLINE</span>
            </div>
          </div>
        </div>

        <div style={{ 
          backgroundColor: 'rgba(30, 41, 59, 0.5)', 
          backdropFilter: 'blur(12px)', 
          borderRadius: '0.75rem', 
          border: '1px solid rgba(55, 65, 81, 1)', 
          padding: '1.5rem', 
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' 
        }}>
          <h3 style={{ 
            fontSize: '1.25rem', 
            fontWeight: 'bold', 
            color: 'white', 
            marginBottom: '1rem', 
            display: 'flex', 
            alignItems: 'center' 
          }}>
            <span style={{ marginRight: '0.75rem' }}>🕒</span>
            RECENT ACTIVITY
          </h3>
          <div style={{ maxHeight: '16rem', overflowY: 'auto' }}>
            {recentActivity.length > 0 ? (
              recentActivity.map((activity, index) => (
                <div key={index} style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '1rem', 
                  padding: '0.75rem', 
                  backgroundColor: 'rgba(55, 65, 81, 0.3)', 
                  borderRadius: '0.5rem', 
                  marginBottom: '0.5rem',
                  transition: 'all 0.2s ease-in-out'
                }}>
                  <div style={{ 
                    flexShrink: '0', 
                    width: '2.5rem', 
                    height: '2.5rem', 
                    borderRadius: '50%', 
                    backgroundColor: activity.color === 'danger' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(245, 158, 11, 0.1)', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center' 
                  }}>
                    <span style={{ fontSize: '1.25rem' }}>{activity.icon}</span>
                  </div>
                  <div style={{ flex: '1', minWidth: '0' }}>
                    <p style={{ fontSize: '0.875rem', color: 'white', margin: 0, wordBreak: 'break-word' }}>
                      {activity.message}
                    </p>
                    <p style={{ fontSize: '0.75rem', color: '#9ca3af', fontFamily: 'monospace', margin: 0 }}>
                      {new Date(activity.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <div style={{ flexShrink: '0' }}>
                    {activity.suspicious_score > 3 ? (
                      <span style={{ color: '#ef4444' }}>⚠️</span>
                    ) : (
                      <span style={{ color: '#22c55e' }}>✅</span>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>👁️</div>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '500', color: '#9ca3af', marginBottom: '0.5rem' }}>
                  No recent activity
                </h3>
                <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                  Start monitoring to see activity here.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
