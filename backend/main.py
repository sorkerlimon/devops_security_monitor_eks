"""
FastAPI main application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import engine, Base
from config import settings
from routers import auth, users, malware, web, network

# Load environment variables from .env file
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Security Monitor API - Network, Malware, and Web Activity Monitoring"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(malware.router, prefix=settings.API_V1_STR)
app.include_router(web.router, prefix=settings.API_V1_STR)
app.include_router(network.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Security Monitor API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
