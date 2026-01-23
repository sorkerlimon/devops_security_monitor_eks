from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .models import UserRole, RoomType, BookingStatus

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price_per_night: float
    description: Optional[str] = None
    is_available: bool = True

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    room_id: int
    check_in_date: datetime
    check_out_date: datetime

class BookingCreate(BookingBase):
    pass

class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in_date: datetime
    check_out_date: datetime
    total_price: float
    booking_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
