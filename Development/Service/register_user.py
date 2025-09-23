"""
User registration script for Security Monitor
"""

import requests
import json

def register_user():
    """Register a new user with the API"""
    print("=" * 50)
    print("Security Monitor - User Registration")
    print("=" * 50)
    
    # Get user details
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return False
    
    email = input("Enter email: ").strip()
    if not email:
        print("Email cannot be empty!")
        return False
    
    full_name = input("Enter full name (optional): ").strip()
    
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty!")
        return False
    
    confirm_password = input("Confirm password: ").strip()
    if password != confirm_password:
        print("Passwords do not match!")
        return False
    
    # Register with API
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/users/register",
            json={
                "username": username,
                "email": email,
                "full_name": full_name,
                "password": password
            }
        )
        
        if response.status_code == 201:
            print("✅ User registered successfully!")
            print(f"Username: {username}")
            print(f"Email: {email}")
            return True
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    register_user()
