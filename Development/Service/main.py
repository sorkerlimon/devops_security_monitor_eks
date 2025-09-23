#!/usr/bin/env python3
"""
Main entry point for the Network Monitor application
"""

import argparse
import sys
import threading
import time
from network_monitor import NetworkMonitor
from malware_detector import MalwareDetector
from web_monitor import WebMonitor

def get_user_credentials():
    """Get username and password from user input"""
    print("=" * 50)
    print("Security Monitor - User Authentication")
    print("=" * 50)
    
    while True:
        username = input("Enter username: ").strip()
        if username:
            break
        print("Username cannot be empty. Please try again.")
    
    while True:
        password = input("Enter password: ").strip()
        if password:
            break
        print("Password cannot be empty. Please try again.")
    
    return username, password

def main():
    """Main function to run the network monitor"""
    parser = argparse.ArgumentParser(description='Real-time Network Monitor')
    parser.add_argument('--host', default='localhost', help='Host to monitor (default: localhost)')
    parser.add_argument('--ports', nargs='+', type=int, help='Specific ports to monitor')
    parser.add_argument('--interval', type=int, default=30, help='Scan interval in seconds (default: 30)')
    parser.add_argument('--duration', type=int, help='Monitoring duration in seconds')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--output', default='network_report.json', help='Output report file')
    parser.add_argument('--log', default='network_monitor.log', help='Log file path')
    parser.add_argument('--status', action='store_true', help='Show current monitoring status and exit')
    parser.add_argument('--malware-only', action='store_true', help='Run only malware detection')
    parser.add_argument('--network-only', action='store_true', help='Run only network monitoring')
    parser.add_argument('--web-only', action='store_true', help='Run only web activity monitoring')
    parser.add_argument('--malware-config', help='Malware detection configuration file')
    parser.add_argument('--web-config', help='Web monitoring configuration file')
    parser.add_argument('--no-auth', action='store_true', help='Skip authentication (for testing)')
    
    args = parser.parse_args()
    
    # Get user credentials if not skipping auth
    username, password = None, None
    if not args.no_auth:
        username, password = get_user_credentials()
    
    # Create monitor instances
    network_monitor = NetworkMonitor(args.config)
    malware_detector = MalwareDetector(args.malware_config)
    web_monitor = WebMonitor(args.web_config)
    
    # Update API credentials if provided
    if username and password:
        network_monitor.config['api_username'] = username
        network_monitor.config['api_password'] = password
        malware_detector.config['api_username'] = username
        malware_detector.config['api_password'] = password
        web_monitor.config['api_username'] = username
        web_monitor.config['api_password'] = password
        
        # Reinitialize API connections with new credentials
        if network_monitor.config['api_enabled']:
            network_monitor._init_api_connection()
        if malware_detector.config['api_enabled']:
            malware_detector._init_api_connection()
        if web_monitor.config['api_enabled']:
            web_monitor._init_api_connection()
    
    # Update network monitor configuration from command line
    if args.ports:
        network_monitor.config['common_ports'] = args.ports
    if args.interval:
        network_monitor.config['scan_interval'] = args.interval
    if args.output:
        network_monitor.config['output_file'] = args.output
    if args.log:
        network_monitor.config['log_file'] = args.log
    
    # Show status if requested
    if args.status:
        network_status = network_monitor.get_status()
        malware_status = malware_detector.get_detection_report()
        web_status = web_monitor.get_monitoring_report()
        
        print("=== Network Monitor Status ===")
        print(f"  Running: {network_status['running']}")
        print(f"  Monitored Ports: {network_status['monitored_ports']}")
        print(f"  Total Alerts: {network_status['total_alerts']}")
        print(f"  Last Scan: {network_status['last_scan']}")
        
        print("\n=== Malware Detection Status ===")
        print(f"  Suspicious Files: {len(malware_status['suspicious_files'])}")
        print(f"  Malware Signatures: {malware_status['malware_signatures_count']}")
        print(f"  Suspicious Domains: {malware_status['suspicious_domains_count']}")
        print(f"  Network Connections: {malware_status['total_network_connections']}")
        
        print("\n=== Web Activity Monitor Status ===")
        print(f"  Running: {web_status['running']}")
        print(f"  Suspicious Sites: {web_status['activity_summary']['suspicious_sites']}")
        print(f"  Blocked Domains: {web_status['activity_summary']['blocked_domains']}")
        print(f"  Allowed Domains: {web_status['activity_summary']['allowed_domains']}")
        print(f"  Total Connections: {web_status['activity_summary']['total_connections']}")
        return
    
    try:
        if args.malware_only:
            # Run only malware detection
            print("\n" + "=" * 50)
            print("Starting Malware Detection Only")
            print("=" * 50)
            print(f"User: {username if username else 'No authentication'}")
            print("Press Ctrl+C to stop detection")
            print("-" * 50)
            malware_detector.run_detection()
            
        elif args.network_only:
            # Run only network monitoring
            print("\n" + "=" * 50)
            print("Starting Network Monitoring Only")
            print("=" * 50)
            print(f"User: {username if username else 'No authentication'}")
            print(f"Monitoring on {args.host}")
            print(f"Ports: {network_monitor.config['common_ports']}")
            print("Press Ctrl+C to stop monitoring")
            print("-" * 50)
            network_monitor.monitor_network(args.host, args.duration)
            
        elif args.web_only:
            # Run only web activity monitoring
            print("\n" + "=" * 50)
            print("Starting Web Activity Monitoring Only")
            print("=" * 50)
            print(f"User: {username if username else 'No authentication'}")
            print("Press Ctrl+C to stop monitoring")
            print("-" * 50)
            web_monitor.run_monitoring()
            
        else:
            # Run all monitoring systems
            print("\n" + "=" * 50)
            print("Starting Comprehensive Security Monitoring")
            print("=" * 50)
            print(f"User: {username if username else 'No authentication'}")
            print(f"Network monitoring on {args.host}")
            print(f"Monitoring ports: {network_monitor.config['common_ports']}")
            print("Malware detection active")
            print("Web activity monitoring active")
            print("API integration enabled")
            print("Press Ctrl+C to stop monitoring")
            print("-" * 50)
            
            # Start all monitors in separate threads
            network_thread = threading.Thread(
                target=network_monitor.monitor_network, 
                args=(args.host, args.duration)
            )
            malware_thread = threading.Thread(target=malware_detector.run_detection)
            web_thread = threading.Thread(target=web_monitor.run_monitoring)
            
            network_thread.daemon = True
            malware_thread.daemon = True
            web_thread.daemon = True
            
            network_thread.start()
            malware_thread.start()
            web_thread.start()
            
            # Wait for threads to complete or keyboard interrupt
            try:
                while network_thread.is_alive() or malware_thread.is_alive() or web_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping all monitoring...")
                network_monitor.stop()
                malware_detector.stop()
                web_monitor.stop()
                network_thread.join(timeout=5)
                malware_thread.join(timeout=5)
                web_thread.join(timeout=5)
        
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
