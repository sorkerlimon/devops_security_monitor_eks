#!/usr/bin/env python3
"""
Generate sample monitoring data for testing the dashboard
"""

import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User, NetworkReport, MalwareReport, WebReport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_sample_data():
    """Generate sample monitoring data"""
    db = SessionLocal()
    
    try:
        # Get the admin user
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("Admin user not found. Please run create_admin.py first.")
            return
        
        print(f"Generating sample data for user: {admin_user.username}")
        
        # Generate sample network reports
        print("Generating network reports...")
        for i in range(50):
            report = NetworkReport(
                user_id=admin_user.id,
                host=f"192.168.1.{random.randint(1, 254)}",
                port=random.randint(1, 65535),
                is_open=random.choice([True, False]),
                status="completed",
                scan_duration=random.uniform(0.1, 2.0),
                created_at=datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
            )
            db.add(report)
        
        # Generate sample malware reports
        print("Generating malware reports...")
        file_extensions = ['.exe', '.dll', '.bat', '.cmd', '.scr', '.com', '.pif', '.vbs', '.js', '.jar']
        suspicious_keywords = ['virus', 'malware', 'trojan', 'backdoor', 'keylogger', 'spyware', 'adware']
        
        for i in range(30):
            file_name = f"suspicious_file_{i}{random.choice(file_extensions)}"
            file_path = f"C:\\Users\\{admin_user.username}\\Downloads\\{file_name}"
            suspicious_score = random.randint(1, 10)
            
            # Add suspicious keywords to some files
            if suspicious_score > 5:
                file_name = f"{random.choice(suspicious_keywords)}_{file_name}"
            
            report = MalwareReport(
                user_id=admin_user.id,
                file_name=file_name,
                file_path=file_path,
                file_size=random.randint(1024, 10485760),  # 1KB to 10MB
                file_hash=f"md5_{random.randint(100000, 999999)}",
                suspicious_score=suspicious_score,
                malware_detected=suspicious_score > 6,
                indicators=[random.choice(suspicious_keywords) for _ in range(random.randint(0, 3))],
                status="analyzed",
                created_at=datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
            )
            db.add(report)
        
        # Generate sample web reports
        print("Generating web reports...")
        domains = [
            'google.com', 'facebook.com', 'youtube.com', 'amazon.com', 'wikipedia.org',
            'github.com', 'stackoverflow.com', 'reddit.com', 'twitter.com', 'linkedin.com',
            'suspicious-site.com', 'malware-download.net', 'phishing-bank.org',
            'crypto-mining.pool', 'torrent-tracker.org', 'adult-content.site'
        ]
        
        for i in range(100):
            domain = random.choice(domains)
            suspicious_score = random.randint(1, 10)
            
            # Make some domains more suspicious
            if 'suspicious' in domain or 'malware' in domain or 'phishing' in domain:
                suspicious_score = random.randint(7, 10)
            
            report = WebReport(
                user_id=admin_user.id,
                domain=domain,
                url=f"https://{domain}/page{random.randint(1, 100)}",
                activity_type=random.choice(['browsing', 'download', 'form_submission', 'api_call']),
                suspicious_score=suspicious_score,
                is_blocked=suspicious_score > 7,
                is_whitelisted=domain in ['google.com', 'github.com', 'stackoverflow.com'],
                category=random.choice(['social', 'shopping', 'news', 'entertainment', 'technology', 'suspicious']),
                created_at=datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
            )
            db.add(report)
        
        # Commit all changes
        db.commit()
        print("Sample data generated successfully!")
        print(f"- {50} network reports")
        print(f"- {30} malware reports")
        print(f"- {100} web reports")
        
    except Exception as e:
        print(f"Error generating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_sample_data()
