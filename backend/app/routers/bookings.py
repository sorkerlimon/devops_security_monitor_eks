from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, models, auth

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Check if room exists
    room = db.query(models.Room).filter(models.Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not room.is_available:
        raise HTTPException(status_code=400, detail="Room is not currently available for booking")
    
    # Calculate price
    duration = (booking.check_out_date - booking.check_in_date).days
    if duration <= 0:
        raise HTTPException(status_code=400, detail="Check-out date must be after check-in date")
    
    total_price = duration * room.price_per_night

    db_booking = models.Booking(
        user_id=current_user.id,
        room_id=booking.room_id,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        total_price=total_price,
        booking_status=models.BookingStatus.CONFIRMED.value
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=List[schemas.BookingResponse])
def get_all_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    bookings = db.query(models.Booking).offset(skip).limit(limit).all()
    return bookings

@router.get("/me", response_model=List[schemas.BookingResponse])
def get_my_bookings(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    bookings = db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()
    return bookings
