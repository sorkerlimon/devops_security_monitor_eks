"""
Configuration settings for the Security Monitor API
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./security_monitor.db")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # API
    API_V1_STR = "/api/v1"
    PROJECT_NAME = "Security Monitor API"
    
    # CORS
    BACKEND_CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://security-monitor.local:3000",
        "https://security-monitor.local:3000",
    ]

settings = Settings()
