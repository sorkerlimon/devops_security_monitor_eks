"""
Script to create the first admin user
"""

import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import SessionLocal, engine
from models import User, Base
from auth import get_password_hash

# Load environment variables from .env file
load_dotenv()

def create_admin_user():
    """Create the first admin user"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            print("Admin user already exists!")
            return
        
        # Get admin credentials from environment variables
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@securitymonitor.com")
        
        # Create admin user
        admin_user = User(
            username=admin_username,
            email=admin_email,
            full_name="System Administrator",
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"Username: {admin_username}")
        print(f"Password: {admin_password}")
        print(f"Email: {admin_email}")
        print("\n⚠️  Please change the password after first login!")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
