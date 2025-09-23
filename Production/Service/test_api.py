"""
Test script to verify API integration
"""

from api_client import APIClient
import json

def test_api_connection():
    """Test API connection and authentication"""
    print("Testing API connection...")
    
    # Create API client
    api_client = APIClient("http://localhost:8000")
    
    # Test connection
    if api_client.test_connection():
        print("✅ API connection successful")
    else:
        print("❌ API connection failed")
        return False
    
    # Test login
    if api_client.login("admin", "admin123"):
        print("✅ Authentication successful")
    else:
        print("❌ Authentication failed")
        return False
    
    # Test sending sample data
    print("\nTesting data sending...")
    
    # Test malware report
    malware_data = {
        "file_path": "/test/suspicious.exe",
        "file_name": "suspicious.exe",
        "file_size": 1024,
        "file_hash_md5": "d41d8cd98f00b204e9800998ecf8427e",
        "file_hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "suspicious_score": 5,
        "malware_detected": False,
        "indicators": '["Suspicious extension: .exe"]',
        "status": "detected"
    }
    
    if api_client.send_malware_report(malware_data):
        print("✅ Malware report sent successfully")
    else:
        print("❌ Failed to send malware report")
    
    # Test web report
    web_data = {
        "domain": "test-suspicious.com",
        "ip_address": "192.168.1.100",
        "port": 80,
        "suspicious_score": 3,
        "category": "suspicious",
        "indicators": '["Contains suspicious keyword: test"]',
        "connection_type": "dns_query",
        "is_blocked": False,
        "is_whitelisted": False
    }
    
    if api_client.send_web_report(web_data):
        print("✅ Web report sent successfully")
    else:
        print("❌ Failed to send web report")
    
    # Test network report
    network_data = {
        "host": "localhost",
        "port": 80,
        "is_open": True,
        "status": "open",
        "scan_duration": 1.0
    }
    
    if api_client.send_network_report(network_data):
        print("✅ Network report sent successfully")
    else:
        print("❌ Failed to send network report")
    
    print("\n🎉 API integration test completed!")
    return True

if __name__ == "__main__":
    test_api_connection()
