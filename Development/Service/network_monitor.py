"""
Real-time Network Monitor and Port Scanner
Monitors network ports, analyzes traffic, and detects network activity
"""

import socket
import threading
import time
import psutil
import logging
import sys
from datetime import datetime
from collections import defaultdict, deque
import json
import os
from api_client import APIClient

class NetworkMonitor:
    def __init__(self, config_file=None):
        self.running = False
        self.monitored_ports = set()
        self.port_status = {}
        self.network_stats = defaultdict(lambda: deque(maxlen=100))
        self.alerts = []
        self.logger = self._setup_logging()
        self.api_client = APIClient()
        self.alerted_ports = {}  # Track recently alerted ports
        
        # Configuration
        self.config = {
            'scan_interval': 30,  # seconds
            'common_ports': [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 6379],
            'alert_threshold': 10,  # connections per minute
            'log_file': 'network_monitor.log',
            'output_file': 'network_report.json',
            'api_enabled': True,
            'api_username': 'admin',
            'api_password': 'admin123',
            'alert_cooldown': 300,  # 5 minutes cooldown
            'report_open_ports_only': True  # Only report open ports to reduce noise
        }
        
        if config_file and os.path.exists(config_file):
            self._load_config(config_file)
        
        # Initialize API connection
        if self.config['api_enabled']:
            self._init_api_connection()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('network_monitor.log'),
                logging.StreamHandler(sys.stdout)
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
            self.api_client.send_network_report(report_data)
        except Exception as e:
            self.logger.error(f"Error sending to API: {e}")
    
    def _should_alert_port(self, host, port):
        """Check if we should alert for this port (cooldown)"""
        current_time = time.time()
        port_key = f"{host}:{port}"
        if port_key in self.alerted_ports:
            last_alert = self.alerted_ports[port_key]
            if current_time - last_alert < self.config['alert_cooldown']:
                return False
        
        self.alerted_ports[port_key] = current_time
        return True
    
    def scan_port(self, host, port, timeout=1):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception as e:
            self.logger.debug(f"Error scanning port {port}: {e}")
            return False
    
    def scan_ports(self, host='localhost', ports=None):
        """Scan multiple ports on a host"""
        if ports is None:
            ports = self.config['common_ports']
        
        open_ports = []
        threads = []
        results = {}
        
        def scan_worker(port):
            is_open = self.scan_port(host, port)
            results[port] = is_open
            if is_open:
                open_ports.append(port)
        
        # Create threads for concurrent scanning
        for port in ports:
            thread = threading.Thread(target=scan_worker, args=(port,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        return open_ports, results
    
    def get_network_connections(self):
        """Get current network connections"""
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    try:
                        process_name = None
                        if conn.pid:
                            try:
                                process_name = psutil.Process(conn.pid).name()
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                process_name = "Unknown"
                        
                        connections.append({
                            'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                            'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                            'status': conn.status,
                            'pid': conn.pid,
                            'process_name': process_name
                        })
                    except Exception as e:
                        self.logger.debug(f"Error processing connection: {e}")
                        continue
        except Exception as e:
            self.logger.error(f"Error getting network connections: {e}")
        
        return connections
    
    def get_network_interface_stats(self):
        """Get network interface statistics"""
        stats = {}
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                if interface != 'lo':  # Skip loopback
                    stats[interface] = {
                        'addresses': [addr.address for addr in addrs if addr.family == socket.AF_INET],
                        'netmask': [addr.netmask for addr in addrs if addr.family == socket.AF_INET],
                        'broadcast': [addr.broadcast for addr in addrs if addr.family == socket.AF_INET]
                    }
            
            # Get I/O statistics
            io_stats = psutil.net_io_counters(pernic=True)
            for interface, io in io_stats.items():
                if interface in stats:
                    stats[interface].update({
                        'bytes_sent': io.bytes_sent,
                        'bytes_recv': io.bytes_recv,
                        'packets_sent': io.packets_sent,
                        'packets_recv': io.packets_recv,
                        'errin': io.errin,
                        'errout': io.errout,
                        'dropin': io.dropin,
                        'dropout': io.dropout
                    })
        except Exception as e:
            self.logger.error(f"Error getting network interface stats: {e}")
        
        return stats
    
    def analyze_network_activity(self):
        """Analyze current network activity"""
        connections = self.get_network_connections()
        interface_stats = self.get_network_interface_stats()
        
        # Count connections by port
        port_counts = defaultdict(int)
        for conn in connections:
            if conn['local_addr'] and ':' in conn['local_addr']:
                try:
                    port_str = conn['local_addr'].split(':')[1]
                    if port_str:  # Check if port string is not empty
                        port = int(port_str)
                        port_counts[port] += 1
                except (ValueError, IndexError) as e:
                    # Skip invalid port formats
                    self.logger.debug(f"Skipping invalid port format: {conn['local_addr']} - {e}")
                    continue
        
        # Detect suspicious activity
        alerts = []
        for port, count in port_counts.items():
            if count > self.config['alert_threshold']:
                alerts.append(f"High connection count on port {port}: {count} connections")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_connections': len(connections),
            'port_counts': dict(port_counts),
            'interface_stats': interface_stats,
            'alerts': alerts
        }
    
    def monitor_network(self, host='localhost', duration=None):
        """Main monitoring loop"""
        self.running = True
        start_time = time.time()
        
        self.logger.info(f"Starting network monitoring on {host}")
        self.logger.info(f"Monitoring ports: {self.config['common_ports']}")
        
        try:
            while self.running:
                try:
                    # Scan ports
                    open_ports, port_results = self.scan_ports(host, self.config['common_ports'])
                    
                    # Analyze network activity
                    activity = self.analyze_network_activity()
                except Exception as e:
                    self.logger.error(f"Error in monitoring cycle: {e}")
                    time.sleep(5)  # Wait before retrying
                    continue
                
                # Update port status and send to API
                for port, is_open in port_results.items():
                    self.port_status[port] = {
                        'open': is_open,
                        'last_checked': datetime.now().isoformat()
                    }
                    
                    # Only send to API if port is open and cooldown allows
                    if is_open and self._should_alert_port(host, port):
                        api_data = {
                            'host': host,
                            'port': port,
                            'is_open': is_open,
                            'status': 'open',
                            'scan_duration': 1.0  # Default timeout
                        }
                        self._send_to_api(api_data)
                
                # Log results
                self.logger.info(f"Open ports: {open_ports}")
                if activity['alerts']:
                    for alert in activity['alerts']:
                        self.logger.warning(alert)
                        self.alerts.append({
                            'timestamp': datetime.now().isoformat(),
                            'message': alert
                        })
                
                # Save periodic report
                if len(self.alerts) % 10 == 0:  # Every 10 alerts
                    self.save_report()
                
                # Check duration limit
                if duration and (time.time() - start_time) >= duration:
                    break
                
                time.sleep(self.config['scan_interval'])
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Error during monitoring: {e}")
        finally:
            self.running = False
            self.save_report()
            self.logger.info("Network monitoring stopped")
    
    def save_report(self):
        """Save monitoring report to file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'port_status': self.port_status,
            'alerts': self.alerts[-50:],  # Keep last 50 alerts
            'config': self.config
        }
        
        try:
            with open(self.config['output_file'], 'w') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False

    def get_status(self):
        """Get current monitoring status"""
        return {
            'running': self.running,
            'monitored_ports': list(self.monitored_ports),
            'port_status': self.port_status,
            'total_alerts': len(self.alerts),
            'last_scan': max([status.get('last_checked', '') for status in self.port_status.values()], default='Never')
        }
