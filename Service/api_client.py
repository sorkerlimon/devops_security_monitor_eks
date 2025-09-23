"""
API Client for sending monitoring data to the backend
"""

import requests
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Set headers
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        else:
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
    
    def set_auth_token(self, token: str):
        """Set authentication token"""
        self.api_key = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def login(self, username: str, password: str) -> bool:
        """Login and get authentication token"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/login-json",
                json={
                    "username": username,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.set_auth_token(data['access_token'])
                self.logger.info("Successfully authenticated with API")
                return True
            else:
                self.logger.error(f"Login failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Login error: {e}")
            return False
    
    def send_malware_report(self, report_data: Dict[str, Any]) -> bool:
        """Send malware detection report to API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/malware/",
                json=report_data
            )
            
            if response.status_code == 201:
                self.logger.debug("Malware report sent successfully")
                return True
            else:
                self.logger.error(f"Failed to send malware report: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending malware report: {e}")
            return False
    
    def send_web_report(self, report_data: Dict[str, Any]) -> bool:
        """Send web activity report to API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/web/",
                json=report_data
            )
            
            if response.status_code == 201:
                self.logger.debug("Web report sent successfully")
                return True
            else:
                self.logger.error(f"Failed to send web report: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending web report: {e}")
            return False
    
    def send_network_report(self, report_data: Dict[str, Any]) -> bool:
        """Send network monitoring report to API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/network/",
                json=report_data
            )
            
            if response.status_code == 201:
                self.logger.debug("Network report sent successfully")
                return True
            else:
                self.logger.error(f"Failed to send network report: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending network report: {e}")
            return False
    
    def get_user_id(self, username: str) -> Optional[int]:
        """Get user ID by username"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/users/me")
            
            if response.status_code == 200:
                data = response.json()
                return data.get('id')
            else:
                self.logger.error(f"Failed to get user ID: {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting user ID: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"API connection test failed: {e}")
            return False
