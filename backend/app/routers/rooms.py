from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, models, auth

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

@router.get("/", response_model=List[schemas.RoomResponse])
def get_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    rooms = db.query(models.Room).offset(skip).limit(limit).all()
    return rooms

@router.get("/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: int, db: Session = Depends(database.get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("/", response_model=schemas.RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: schemas.RoomCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    db_room = db.query(models.Room).filter(models.Room.room_number == room.room_number).first()
    if db_room:
        raise HTTPException(status_code=400, detail="Room number already exists")

    db_room = models.Room(
        room_number=room.room_number,
        room_type=room.room_type,
        price_per_night=room.price_per_night,
        description=room.description,
        is_available=room.is_available
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.put("/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: int, room: schemas.RoomCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db_room.room_number = room.room_number
    db_room.room_type = room.room_type
    db_room.price_per_night = room.price_per_night
    db_room.description = room.description
    db_room.is_available = room.is_available
    
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db.delete(db_room)
    db.commit()
    return None
