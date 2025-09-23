# Real-time Network Monitor & Malware Detection System

A comprehensive Python security monitoring system that monitors network ports, analyzes real-time network activity, and detects malware threats including suspicious files, network connections, and process anomalies.

## Features

### Network Monitoring
- **Port Scanning**: Continuously scans common ports for open/closed status
- **Network Connection Monitoring**: Tracks active network connections
- **Interface Statistics**: Monitors network interface I/O statistics
- **Real-time Analysis**: Detects unusual network activity patterns
- **Alerting System**: Generates alerts for suspicious activity
- **Multi-threaded**: Concurrent port scanning for better performance

### Malware Detection
- **File Monitoring**: Scans download directories for suspicious files
- **Hash Analysis**: Calculates and checks file hashes against malware database
- **Suspicious File Detection**: Identifies files with suspicious extensions and patterns
- **Process Anomaly Detection**: Monitors for suspicious process behavior
- **Network Threat Detection**: Identifies malicious network connections and domains
- **Real-time Scanning**: Continuous monitoring of system activity
- **Threat Intelligence**: Integration with external threat intelligence feeds

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## File Structure

```
Network/
├── main.py                    # Main entry point
├── network_monitor.py         # Network monitoring module
├── malware_detector.py        # Malware detection module
├── config.json               # Network monitoring configuration
├── malware_config.json       # Malware detection configuration
├── malware_signatures.json   # Malware signature database
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Usage

### Basic Usage
```bash
# Run both network monitoring and malware detection
python main.py
```

### Advanced Usage
```bash
# Run only network monitoring
python main.py --network-only

# Run only malware detection
python main.py --malware-only

# Monitor specific ports
python main.py --ports 80 443 22 21

# Monitor for specific duration (in seconds)
python main.py --duration 300

# Use custom configuration files
python main.py --config config.json --malware-config malware_config.json

# Monitor remote host
python main.py --host 192.168.1.1

# Custom scan interval (seconds) - default is 60
python main.py --interval 30

# Check monitoring status
python main.py --status
```

### Command Line Options

#### Network Monitoring
- `--host`: Host to monitor (default: localhost)
- `--ports`: Specific ports to monitor (space-separated)
- `--interval`: Scan interval in seconds (default: 60)
- `--duration`: Monitoring duration in seconds (optional)
- `--config`: Network monitoring configuration file
- `--output`: Output report file (default: network_report.json)
- `--log`: Log file path (default: network_monitor.log)

#### Malware Detection
- `--malware-only`: Run only malware detection
- `--network-only`: Run only network monitoring
- `--malware-config`: Malware detection configuration file

#### General
- `--status`: Show current monitoring status and exit

## Configuration

The system uses separate configuration files for network monitoring and malware detection.

### Network Monitoring Configuration (`config.json`)
```json
{
  "scan_interval": 60,
  "common_ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 6379],
  "alert_threshold": 10,
  "log_file": "network_monitor.log",
  "output_file": "network_report.json"
}
```

### Malware Detection Configuration (`malware_config.json`)
```json
{
  "scan_interval": 10,
  "download_paths": ["~/Downloads", "~/Desktop", "C:\\Users\\Public\\Downloads"],
  "suspicious_extensions": [".exe", ".bat", ".cmd", ".scr", ".pif", ".com", ".vbs", ".js", ".jar"],
  "max_file_size": 104857600,
  "malware_db_file": "malware_signatures.json",
  "alert_threshold": 5,
  "enable_hash_checking": true,
  "enable_domain_checking": true
}
```

## Output Files

### Network Monitoring
- **network_monitor.log**: Detailed log of all network monitoring activities
- **network_report.json**: JSON report containing port status, alerts, and statistics

### Malware Detection
- **malware_detector.log**: Detailed log of malware detection activities
- **malware_signatures.json**: Database of known malware signatures
- **malware_report.json**: JSON report containing detected threats and suspicious files

## Monitoring Capabilities

### Network Monitoring
- **Port Scanning**: Scans common ports (HTTP, HTTPS, SSH, FTP, etc.)
- **Connection Tracking**: Monitors active network connections
- **Process Identification**: Identifies which processes are using network connections
- **Interface Statistics**: Tracks network I/O, packet counts, and error rates
- **Traffic Analysis**: Analyzes network traffic patterns and anomalies

### Malware Detection
- **File Monitoring**: Scans download directories for suspicious files
- **Hash Analysis**: Calculates MD5/SHA256 hashes and checks against malware database
- **Suspicious File Detection**: Identifies files with suspicious extensions and patterns
- **Process Anomaly Detection**: Monitors for suspicious process behavior
- **Network Threat Detection**: Identifies malicious network connections and domains
- **Threat Intelligence**: Integration with external threat intelligence feeds

### Alert System
- **Network Alerts**: High connection count detection, suspicious activity alerts
- **Malware Alerts**: Suspicious file detection, malware signature matches
- **Process Alerts**: Process anomalies, suspicious command execution
- **Configurable Thresholds**: Customizable alert sensitivity levels

## Example Output

### Network Monitoring
```
2024-01-15 10:30:15 - INFO - Starting network monitoring on localhost
2024-01-15 10:30:15 - INFO - Monitoring ports: [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 6379]
2024-01-15 10:30:20 - INFO - Open ports: [80, 443, 22]
2024-01-15 10:30:25 - WARNING - High connection count on port 80: 15 connections
```

### Malware Detection
```
2024-01-15 10:30:15 - MALWARE - INFO - Starting malware detection
2024-01-15 10:30:20 - MALWARE - WARNING - Suspicious file detected: C:\Users\User\Downloads\suspicious.exe
2024-01-15 10:30:20 - MALWARE - WARNING - Score: 5, Indicators: ['Suspicious extension: .exe', 'Suspicious filename pattern']
2024-01-15 10:30:25 - MALWARE - WARNING - Network threat detected: {'type': 'suspicious_port', 'remote': '192.168.1.100:4444'}
2024-01-15 10:30:30 - MALWARE - CRITICAL - MALWARE DETECTED: C:\Users\User\Downloads\malware.exe
```

### Status Check
```
=== Network Monitor Status ===
  Running: False
  Monitored Ports: [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 6379]
  Total Alerts: 3
  Last Scan: 2024-01-15T10:30:20

=== Malware Detection Status ===
  Suspicious Files: 2
  Malware Signatures: 1000
  Suspicious Domains: 5000
  Network Connections: 45
```

## Requirements

- Python 3.7+
- psutil library
- requests library
- Windows/Linux/macOS support

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run complete security monitoring:**
   ```bash
   python main.py
   ```

3. **Check status:**
   ```bash
   python main.py --status
   ```

4. **Run only malware detection:**
   ```bash
   python main.py --malware-only
   ```

5. **Run only network monitoring:**
   ```bash
   python main.py --network-only
   ```
# Malware only
python main.py --malware-only

# Network only  
python main.py --network-only

# Web only
python main.py --web-only
## Security Note

This tool is designed for legitimate network monitoring and security analysis. Ensure you have proper authorization before monitoring networks you don't own or manage.
