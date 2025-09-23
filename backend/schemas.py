"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Malware schemas
class MalwareReportBase(BaseModel):
    file_path: str
    file_name: str
    file_size: Optional[int] = None
    file_hash_md5: Optional[str] = None
    file_hash_sha256: Optional[str] = None
    suspicious_score: int = 0
    malware_detected: bool = False
    indicators: Optional[str] = None
    process_name: Optional[str] = None
    process_pid: Optional[int] = None
    status: str = "detected"

class MalwareReportCreate(MalwareReportBase):
    pass

class MalwareReportUpdate(BaseModel):
    status: Optional[str] = None
    indicators: Optional[str] = None

class MalwareReport(MalwareReportBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Web monitoring schemas
class WebReportBase(BaseModel):
    domain: str
    ip_address: Optional[str] = None
    port: Optional[int] = None
    browser_name: Optional[str] = None
    process_pid: Optional[int] = None
    suspicious_score: int = 0
    category: Optional[str] = None
    indicators: Optional[str] = None
    connection_type: Optional[str] = None
    is_blocked: bool = False
    is_whitelisted: bool = False

class WebReportCreate(WebReportBase):
    pass

class WebReportUpdate(BaseModel):
    is_blocked: Optional[bool] = None
    is_whitelisted: Optional[bool] = None
    category: Optional[str] = None

class WebReport(WebReportBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Network monitoring schemas
class NetworkReportBase(BaseModel):
    host: str
    port: int
    is_open: bool = False
    service_name: Optional[str] = None
    connection_count: int = 0
    local_address: Optional[str] = None
    remote_address: Optional[str] = None
    process_name: Optional[str] = None
    process_pid: Optional[int] = None
    status: str = "scanned"
    scan_duration: Optional[float] = None

class NetworkReportCreate(NetworkReportBase):
    pass

class NetworkReportUpdate(BaseModel):
    status: Optional[str] = None
    connection_count: Optional[int] = None

class NetworkReport(NetworkReportBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# System stats schemas
class SystemStatsBase(BaseModel):
    total_malware_detected: int = 0
    total_suspicious_sites: int = 0
    total_network_connections: int = 0
    total_ports_scanned: int = 0
    active_users: int = 0
    system_uptime: Optional[float] = None
    last_scan_time: Optional[datetime] = None

class SystemStats(SystemStatsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Dashboard schemas
class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_malware_detected: int
    total_suspicious_sites: int
    total_network_connections: int
    recent_malware: List[MalwareReport]
    recent_web_activity: List[WebReport]
    recent_network_activity: List[NetworkReport]

# Response schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int
