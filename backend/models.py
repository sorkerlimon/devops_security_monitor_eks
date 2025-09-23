"""
Database models for Security Monitor API
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    malware_reports = relationship("MalwareReport", back_populates="user")
    web_reports = relationship("WebReport", back_populates="user")
    network_reports = relationship("NetworkReport", back_populates="user")

class MalwareReport(Base):
    __tablename__ = "malware_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)
    file_hash_md5 = Column(String(32))
    file_hash_sha256 = Column(String(64))
    suspicious_score = Column(Integer, default=0)
    malware_detected = Column(Boolean, default=False)
    indicators = Column(Text)  # JSON string of indicators
    process_name = Column(String(255))
    process_pid = Column(Integer)
    status = Column(String(50), default="detected")  # detected, quarantined, cleaned
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="malware_reports")

class WebReport(Base):
    __tablename__ = "web_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    domain = Column(String(255), nullable=False)
    ip_address = Column(String(45))
    port = Column(Integer)
    browser_name = Column(String(100))
    process_pid = Column(Integer)
    suspicious_score = Column(Integer, default=0)
    category = Column(String(50))  # allowed, blocked, suspicious, normal
    indicators = Column(Text)  # JSON string of indicators
    connection_type = Column(String(50))  # dns_query, browser_connection, network_connection
    is_blocked = Column(Boolean, default=False)
    is_whitelisted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="web_reports")

class NetworkReport(Base):
    __tablename__ = "network_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    is_open = Column(Boolean, default=False)
    service_name = Column(String(100))
    connection_count = Column(Integer, default=0)
    local_address = Column(String(45))
    remote_address = Column(String(45))
    process_name = Column(String(255))
    process_pid = Column(Integer)
    status = Column(String(50), default="scanned")  # scanned, open, closed, filtered
    scan_duration = Column(Float)  # seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="network_reports")

class SystemStats(Base):
    __tablename__ = "system_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    total_malware_detected = Column(Integer, default=0)
    total_suspicious_sites = Column(Integer, default=0)
    total_network_connections = Column(Integer, default=0)
    total_ports_scanned = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    system_uptime = Column(Float)  # seconds
    last_scan_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
