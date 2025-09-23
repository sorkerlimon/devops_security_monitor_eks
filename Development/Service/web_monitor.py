"""
Web Activity Monitor
Tracks user web browsing activity and detects unauthorized or suspicious websites
"""

import os
import json
import time
import threading
import psutil
import socket
import requests
import re
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging
import subprocess
import platform
from urllib.parse import urlparse
import dns.resolver
from api_client import APIClient

class WebMonitor:
    def __init__(self, config_file=None):
        self.logger = self._setup_logging()
        self.running = False
        self.web_activity = deque(maxlen=1000)
        self.suspicious_sites = []
        self.blocked_domains = set()
        self.allowed_domains = set()
        self.user_activity = defaultdict(list)
        self.api_client = APIClient()
        self.alerted_domains = {}  # Track recently alerted domains
        
        # Configuration
        self.config = {
            'scan_interval': 10,  # seconds
            'dns_monitor': True,
            'browser_monitor': True,
            'network_monitor': True,
            'blacklist_file': 'blocked_sites.json',
            'whitelist_file': 'allowed_sites.json',
            'suspicious_keywords': [
                'gambling', 'casino', 'betting', 'porn', 'adult', 'hack', 'crack',
                'torrent', 'pirate', 'illegal', 'drug', 'weapon', 'violence'
            ],
            'legitimate_domains': [
                'amazonaws.com', 'compute-1.amazonaws.com', 'compute.amazonaws.com',
                'github.com', 'githubusercontent.com', 'github.io',
                'lastpass.com', 'cloudfront.net', 'elevohost.com',
                'google.com', 'googleapis.com', 'gstatic.com',
                'microsoft.com', 'office.com', 'live.com',
                'stackoverflow.com', 'wikipedia.org', 'youtube.com',
                'facebook.com', 'twitter.com', 'linkedin.com'
            ],
            'suspicious_tlds': ['.tk', '.ml', '.ga', '.cf', '.bit', '.onion'],
            'max_connections_per_minute': 50,
            'alert_threshold': 5,
            'log_file': 'web_monitor.log',
            'output_file': 'web_report.json',
            'api_enabled': True,
            'api_username': 'admin',
            'api_password': 'admin123',
            'alert_cooldown': 300  # 5 minutes cooldown for same domain
        }
        
        if config_file and os.path.exists(config_file):
            self._load_config(config_file)
        
        self._load_blacklist()
        self._load_whitelist()
        
        # Initialize API connection
        if self.config['api_enabled']:
            self._init_api_connection()
    
    def _setup_logging(self):
        """Setup logging for web monitoring"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - WEB - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('web_monitor.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                self.config.update(config_data)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
    
    def _load_blacklist(self):
        """Load blocked domains from file"""
        try:
            if os.path.exists(self.config['blacklist_file']):
                with open(self.config['blacklist_file'], 'r') as f:
                    data = json.load(f)
                    self.blocked_domains = set(data.get('blocked_domains', []))
                    self.logger.info(f"Loaded {len(self.blocked_domains)} blocked domains")
        except Exception as e:
            self.logger.error(f"Error loading blacklist: {e}")
    
    def _load_whitelist(self):
        """Load allowed domains from file"""
        try:
            if os.path.exists(self.config['whitelist_file']):
                with open(self.config['whitelist_file'], 'r') as f:
                    data = json.load(f)
                    self.allowed_domains = set(data.get('allowed_domains', []))
                    self.logger.info(f"Loaded {len(self.allowed_domains)} allowed domains")
        except Exception as e:
            self.logger.error(f"Error loading whitelist: {e}")
    
    def _init_api_connection(self):
        """Initialize API connection"""
        try:
            if self.api_client.login(self.config['api_username'], self.config['api_password']):
                self.logger.info("API connection established")
            else:
                self.logger.warning("Failed to connect to API")
        except Exception as e:
            self.logger.error(f"API connection error: {e}")
    
    def _send_to_api(self, report_data):
        """Send report data to API"""
        if not self.config['api_enabled']:
            return
        
        try:
            self.api_client.send_web_report(report_data)
        except Exception as e:
            self.logger.error(f"Error sending to API: {e}")
    
    def _should_alert(self, domain):
        """Check if we should alert for this domain (cooldown)"""
        current_time = time.time()
        if domain in self.alerted_domains:
            last_alert = self.alerted_domains[domain]
            if current_time - last_alert < self.config['alert_cooldown']:
                return False
        
        self.alerted_domains[domain] = current_time
        return True
    
    def get_dns_queries(self):
        """Get DNS queries from all network connections"""
        dns_queries = []
        seen_connections = set()  # Track already processed connections
        
        try:
            # Get all network connections using psutil (more reliable)
            for conn in psutil.net_connections(kind='inet'):
                if conn.raddr and conn.status == 'ESTABLISHED':
                    # Create unique identifier for this connection
                    conn_id = f"{conn.raddr.ip}:{conn.raddr.port}"
                    
                    # Skip if we've already processed this connection
                    if conn_id in seen_connections:
                        continue
                    seen_connections.add(conn_id)
                    
                    ip = conn.raddr.ip
                    port = conn.raddr.port
                    
                    # Skip localhost and private IPs that aren't web traffic
                    if (ip in ['127.0.0.1', '::1'] or 
                        ip.startswith('192.168.') or 
                        ip.startswith('10.') or 
                        ip.startswith('172.16.') or
                        ip == '0.0.0.0'):
                        continue
                    
                    # Only monitor common web ports
                    if port not in [80, 443, 8080, 8443, 3000, 5000, 8000, 9000]:
                        continue
                    
                    try:
                        # Try to resolve IP to domain name
                        hostname = socket.gethostbyaddr(ip)[0]
                        
                        # Clean up hostname (remove trailing dots)
                        hostname = hostname.rstrip('.')
                        
                        dns_queries.append({
                            'domain': hostname,
                            'ip': ip,
                            'port': port,
                            'timestamp': datetime.now().isoformat(),
                            'connection_type': 'network'
                        })
                        
                        self.logger.debug(f"Resolved {ip}:{port} -> {hostname}")
                        
                    except socket.herror:
                        # If reverse DNS fails, still log the IP
                        dns_queries.append({
                            'domain': ip,
                            'ip': ip,
                            'port': port,
                            'timestamp': datetime.now().isoformat(),
                            'connection_type': 'network'
                        })
                        
                    except Exception as e:
                        self.logger.debug(f"Error resolving {ip}: {e}")
                        continue
        
        except Exception as e:
            self.logger.error(f"Error getting DNS queries: {e}")
        
        return dns_queries
    
    def get_browser_processes(self):
        """Get active browser processes and their network connections"""
        browser_processes = []
        browser_names = ['chrome', 'firefox', 'edge', 'safari', 'opera', 'brave', 'chromium']
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_info = proc.info
                    if proc_info['name'] and any(browser in proc_info['name'].lower() for browser in browser_names):
                        connections = []
                        try:
                            # Get connections for this specific process
                            proc_connections = proc.connections()
                            for conn in proc_connections:
                                if conn.raddr and conn.status == 'ESTABLISHED':
                                    try:
                                        hostname = socket.gethostbyaddr(conn.raddr.ip)[0]
                                        connections.append({
                                            'domain': hostname,
                                            'ip': conn.raddr.ip,
                                            'port': conn.raddr.port,
                                            'local_port': conn.laddr.port if conn.laddr else None
                                        })
                                    except:
                                        connections.append({
                                            'domain': conn.raddr.ip,
                                            'ip': conn.raddr.ip,
                                            'port': conn.raddr.port,
                                            'local_port': conn.laddr.port if conn.laddr else None
                                        })
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            # Process may have ended or we don't have permission
                            pass
                        
                        browser_processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cmdline': ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else '',
                            'connections': connections,
                            'timestamp': datetime.now().isoformat()
                        })
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        except Exception as e:
            self.logger.error(f"Error getting browser processes: {e}")
        
        return browser_processes
    
    def analyze_domain(self, domain):
        """Analyze a domain for suspicious characteristics"""
        if not domain or domain in ['localhost', '127.0.0.1']:
            return None
        
        analysis = {
            'domain': domain,
            'suspicious_score': 0,
            'indicators': [],
            'category': 'unknown'
        }
        
        # Check against blacklist
        if domain in self.blocked_domains:
            analysis['suspicious_score'] += 10
            analysis['indicators'].append("Domain is blacklisted")
            analysis['category'] = 'blocked'
            return analysis
        
        # Check against whitelist
        if domain in self.allowed_domains:
            analysis['category'] = 'allowed'
            return analysis
        
        # Check against legitimate domains
        for legit_domain in self.config['legitimate_domains']:
            if legit_domain in domain:
                analysis['category'] = 'legitimate'
                return analysis
        
        # Check for suspicious keywords
        domain_lower = domain.lower()
        for keyword in self.config['suspicious_keywords']:
            if keyword in domain_lower:
                analysis['suspicious_score'] += 3
                analysis['indicators'].append(f"Contains suspicious keyword: {keyword}")
                analysis['category'] = 'suspicious'
        
        # Check for suspicious TLDs
        for tld in self.config['suspicious_tlds']:
            if domain.endswith(tld):
                analysis['suspicious_score'] += 2
                analysis['indicators'].append(f"Suspicious TLD: {tld}")
                analysis['category'] = 'suspicious'
        
        # Check for IP addresses (direct IP access)
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
            analysis['suspicious_score'] += 1
            analysis['indicators'].append("Direct IP access")
            analysis['category'] = 'suspicious'
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'[0-9]{8,}',  # Long number sequences
            r'[a-f0-9]{32,}',  # Hash-like names
            r'[a-z]{1,3}\.[a-z]{2,4}$',  # Very short domains
            r'.*\.tk$',  # .tk domains
            r'.*\.ml$',  # .ml domains
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, domain_lower):
                analysis['suspicious_score'] += 2
                analysis['indicators'].append(f"Suspicious pattern: {pattern}")
                analysis['category'] = 'suspicious'
        
        # Only flag as suspicious if score is high enough
        if analysis['suspicious_score'] >= 3:
            analysis['category'] = 'suspicious'
        elif analysis['suspicious_score'] == 0:
            analysis['category'] = 'normal'
        
        return analysis
    
    def monitor_web_activity(self):
        """Monitor web browsing activity"""
        try:
            # Get DNS queries
            if self.config['dns_monitor']:
                dns_queries = self.get_dns_queries()
                for query in dns_queries:
                    analysis = self.analyze_domain(query['domain'])
                    
                    # Log ALL website visits to API, not just suspicious ones
                    api_data = {
                        'domain': query['domain'],
                        'ip_address': query['ip'],
                        'port': int(query['port']) if str(query['port']).isdigit() else None,
                        'suspicious_score': analysis['suspicious_score'] if analysis else 0,
                        'category': analysis['category'] if analysis else 'normal',
                        'indicators': json.dumps(analysis['indicators']) if analysis else '[]',
                        'connection_type': 'dns_query',
                        'is_blocked': analysis['category'] == 'blocked' if analysis else False,
                        'is_whitelisted': analysis['category'] == 'allowed' if analysis else False
                    }
                    self._send_to_api(api_data)
                    
                    # Log to console
                    if analysis and analysis['suspicious_score'] >= 3:
                        self.logger.warning(f"Suspicious DNS query: {query['domain']} (Score: {analysis['suspicious_score']})")
                        suspicious_site = {
                            'type': 'dns_query',
                            'domain': query['domain'],
                            'ip': query['ip'],
                            'port': query['port'],
                            'analysis': analysis,
                            'timestamp': query['timestamp']
                        }
                        self.suspicious_sites.append(suspicious_site)
                    else:
                        self.logger.info(f"Web activity: {query['domain']} (Score: {analysis['suspicious_score'] if analysis else 0})")
            
            # Get browser processes
            if self.config['browser_monitor']:
                browser_processes = self.get_browser_processes()
                for browser in browser_processes:
                    for conn in browser['connections']:
                        analysis = self.analyze_domain(conn['domain'])
                        
                        # Log ALL browser activity to API
                        api_data = {
                            'domain': conn['domain'],
                            'ip_address': conn['ip'],
                            'port': int(conn['port']) if str(conn['port']).isdigit() else None,
                            'suspicious_score': analysis['suspicious_score'] if analysis else 0,
                            'category': analysis['category'] if analysis else 'normal',
                            'indicators': json.dumps(analysis['indicators']) if analysis else '[]',
                            'connection_type': 'browser_connection',
                            'is_blocked': analysis['category'] == 'blocked' if analysis else False,
                            'is_whitelisted': analysis['category'] == 'allowed' if analysis else False
                        }
                        self._send_to_api(api_data)
                        
                        # Log to console
                        if analysis and analysis['suspicious_score'] >= 3:
                            self.logger.warning(f"Suspicious browser activity: {browser['name']} -> {conn['domain']} (Score: {analysis['suspicious_score']})")
                            self.suspicious_sites.append({
                                'type': 'browser_connection',
                                'browser': browser['name'],
                                'pid': browser['pid'],
                                'domain': conn['domain'],
                                'ip': conn['ip'],
                                'port': conn['port'],
                                'analysis': analysis,
                                'timestamp': browser['timestamp']
                            })
                        else:
                            self.logger.info(f"Browser activity: {browser['name']} -> {conn['domain']} (Score: {analysis['suspicious_score'] if analysis else 0})")
            
            # Get network connections
            if self.config['network_monitor']:
                connections = psutil.net_connections(kind='inet')
                for conn in connections:
                    if conn.raddr and conn.status == 'ESTABLISHED':
                        try:
                            hostname = socket.gethostbyaddr(conn.raddr.ip)[0]
                            analysis = self.analyze_domain(hostname)
                            
                            # Log ALL network activity to API
                            api_data = {
                                'domain': hostname,
                                'ip_address': conn.raddr.ip,
                                'port': conn.raddr.port,
                                'suspicious_score': analysis['suspicious_score'] if analysis else 0,
                                'category': analysis['category'] if analysis else 'normal',
                                'indicators': json.dumps(analysis['indicators']) if analysis else '[]',
                                'connection_type': 'network_connection',
                                'is_blocked': analysis['category'] == 'blocked' if analysis else False,
                                'is_whitelisted': analysis['category'] == 'allowed' if analysis else False
                            }
                            self._send_to_api(api_data)
                            
                            # Log to console
                            if analysis and analysis['suspicious_score'] >= 3:
                                self.logger.warning(f"Suspicious network connection: {hostname} (Score: {analysis['suspicious_score']})")
                                self.suspicious_sites.append({
                                    'type': 'network_connection',
                                    'domain': hostname,
                                    'ip': conn.raddr.ip,
                                    'port': conn.raddr.port,
                                    'local_port': conn.laddr.port if conn.laddr else None,
                                    'analysis': analysis,
                                    'timestamp': datetime.now().isoformat()
                                })
                            else:
                                self.logger.info(f"Network activity: {hostname} (Score: {analysis['suspicious_score'] if analysis else 0})")
                        except:
                            pass
        
        except Exception as e:
            self.logger.error(f"Error monitoring web activity: {e}")
    
    def get_user_activity_summary(self):
        """Get summary of user web activity"""
        summary = {
            'total_connections': len(self.web_activity),
            'suspicious_sites': len(self.suspicious_sites),
            'blocked_domains': len(self.blocked_domains),
            'allowed_domains': len(self.allowed_domains),
            'recent_activity': list(self.web_activity)[-10:],  # Last 10 activities
            'top_domains': self._get_top_domains(),
            'suspicious_by_category': self._get_suspicious_by_category()
        }
        return summary
    
    def _get_top_domains(self):
        """Get most frequently accessed domains"""
        domain_counts = defaultdict(int)
        for activity in self.web_activity:
            if 'domain' in activity:
                domain_counts[activity['domain']] += 1
        
        return dict(sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _get_suspicious_by_category(self):
        """Get suspicious sites grouped by category"""
        categories = defaultdict(list)
        for site in self.suspicious_sites:
            if 'analysis' in site and 'category' in site['analysis']:
                categories[site['analysis']['category']].append(site)
        
        return dict(categories)
    
    def run_monitoring(self):
        """Run web activity monitoring"""
        self.running = True
        self.logger.info("Starting web activity monitoring")
        
        try:
            while self.running:
                self.monitor_web_activity()
                
                # Update activity log
                current_time = datetime.now()
                self.web_activity.append({
                    'timestamp': current_time.isoformat(),
                    'suspicious_count': len(self.suspicious_sites),
                    'total_connections': len(psutil.net_connections(kind='inet'))
                })
                
                time.sleep(self.config['scan_interval'])
                
        except KeyboardInterrupt:
            self.logger.info("Web monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Error during web monitoring: {e}")
        finally:
            self.running = False
    
    def get_monitoring_report(self):
        """Get current monitoring report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'running': self.running,
            'suspicious_sites': self.suspicious_sites[-50:],  # Last 50 suspicious sites
            'activity_summary': self.get_user_activity_summary(),
            'config': self.config
        }
    
    def add_to_blacklist(self, domain):
        """Add domain to blacklist"""
        self.blocked_domains.add(domain)
        self._save_blacklist()
        self.logger.info(f"Added {domain} to blacklist")
    
    def add_to_whitelist(self, domain):
        """Add domain to whitelist"""
        self.allowed_domains.add(domain)
        self._save_whitelist()
        self.logger.info(f"Added {domain} to whitelist")
    
    def _save_blacklist(self):
        """Save blacklist to file"""
        try:
            with open(self.config['blacklist_file'], 'w') as f:
                json.dump({'blocked_domains': list(self.blocked_domains)}, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving blacklist: {e}")
    
    def _save_whitelist(self):
        """Save whitelist to file"""
        try:
            with open(self.config['whitelist_file'], 'w') as f:
                json.dump({'allowed_domains': list(self.allowed_domains)}, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving whitelist: {e}")
    
    def stop(self):
        """Stop web monitoring"""
        self.running = False
