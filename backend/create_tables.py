# backend/create_tables.py
import os
from main import Base, engine, User, SessionLocal, pwd_context

def init_db():
    print("Creating database tables if not exist...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            print("No users found. Creating default admin user...")
            admin_user = User(
                username="admin",
                email="admin@getcovered.io",
                hashed_password=pwd_context.hash("admin123"),
                role="admin"  
            )
            db.add(admin_user)
            db.commit()
            print("Default admin user created ✅ (username: admin, password: admin123, role: admin)")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
