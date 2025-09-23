"""
Test database connection
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./security_monitor.db")
print(f"Database URL: {DATABASE_URL}")

try:
    # Create engine
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Database connection successful!")
        print(f"Result: {result.fetchone()}")
        
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
