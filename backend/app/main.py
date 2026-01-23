from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, rooms, bookings, users

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Booking System")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Hotel Booking System API"}
