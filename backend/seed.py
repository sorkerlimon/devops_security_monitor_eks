from app.database import SessionLocal, engine, Base
from app import models, auth

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def create_admin():
    db = SessionLocal()
    email = "admin@example.com"
    password = "admin"
    
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            print(f"Admin user '{email}' already exists.")
        else:
            hashed_password = auth.get_password_hash(password)
            admin_user = models.User(
                name="Admin User",
                email=email,
                password=hashed_password,
                role=models.UserRole.ADMIN.value
            )
            db.add(admin_user)
            db.commit()
            print(f"Admin user '{email}' created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
