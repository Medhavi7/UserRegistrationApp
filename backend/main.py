# backend/main.py
import os
import logging
import time
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import OperationalError
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import jwt
from starlette.responses import RedirectResponse
import authlib.integrations.starlette_client as starlette_client

# -------------------------
# Config
# -------------------------
ALLOWED_EMAIL_DOMAIN = os.getenv("ALLOWED_EMAIL_DOMAIN", "getcovered.io")

# Use DATABASE_URL for Heroku PostgreSQL, fallback to MySQL for local development
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Heroku PostgreSQL
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    # Local MySQL development
    DB_USER = os.getenv("MYSQL_USER", "getcovered")
    DB_PASS = os.getenv("MYSQL_PASSWORD", "strongpassword")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_NAME = os.getenv("MYSQL_DATABASE", "getcovered_db")
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "sessionsecretkey")

# Default admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", f"admin@{ALLOWED_EMAIL_DOMAIN}")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# -------------------------
# Database Setup
# -------------------------
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(50), default="client")
    first_name = Column(String(50), default="")
    last_name = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

# -------------------------
# Security
# -------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="GetCovered API", docs_url="/docs")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# Mount static files (React build)
import os
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "build")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=os.path.join(static_dir, "static")), name="static")

# Configure CORS for production and development
allowed_origins = ["http://localhost:3000"]
if os.getenv("FRONTEND_URL"):
    allowed_origins.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Google OAuth Setup
# -------------------------
oauth = starlette_client.OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# -------------------------
# Utils
# -------------------------
def enforce_email_domain(email: str):
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    domain = email.split("@")[-1].lower()
    if domain != ALLOWED_EMAIL_DOMAIN.lower():
        raise HTTPException(
            status_code=403,
            detail=f"Only {ALLOWED_EMAIL_DOMAIN} emails are allowed"
        )

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------------
# Schemas
# -------------------------
class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class RegisterModel(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    first_name: str
    last_name: str
    created_at: datetime = None
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: str = None
    last_name: str = None

# -------------------------
# Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Startup
# -------------------------
@app.on_event("startup")
def on_startup():
    logging.info("Waiting for database to be ready...")
    db_ready = False
    while not db_ready:
        try:
            engine.connect()
            db_ready = True
            logging.info("Database is ready ✅")
        except OperationalError:
            logging.info("Database not ready, waiting 2s...")
            time.sleep(2)

    logging.info("Creating database tables if they do not exist...")
    Base.metadata.create_all(bind=engine)

    # --- Seed Admin User ---
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == ADMIN_USERNAME).first()
        if not admin_user:
            logging.info("Seeding default admin user...")
            admin = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                hashed_password=pwd_context.hash(ADMIN_PASSWORD),
                role="admin",
                first_name="System",
                last_name="Administrator"
            )
            db.add(admin)
            db.commit()
            logging.info(
                f"✅ Admin user created: username='{ADMIN_USERNAME}', password='{ADMIN_PASSWORD}'"
            )
        else:
            logging.info("Admin user already exists ✅")
    finally:
        db.close()

# -------------------------
# Routes
# -------------------------
@app.post("/register", response_model=Token)
def register(user: RegisterModel, db: Session = Depends(get_db)):
    enforce_email_domain(user.email)
    existing = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=pwd_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"sub": new_user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
    }

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    enforce_email_domain(user.email)
    token = create_access_token({"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }

@app.get("/users/me", response_model=UserOut)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    current_user = db.query(User).filter(User.username == username).first()
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return db.query(User).all()

@app.put("/users/me", response_model=UserOut)
def update_user_profile(user_update: UserUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only the provided fields
    if user_update.first_name is not None:
        user.first_name = user_update.first_name
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
    
    db.commit()
    db.refresh(user)
    return user

# -------------------------
# Google OAuth Routes
# -------------------------
@app.get("/login/google")
async def login_google(request: Request):
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    redirect_uri = f"{base_url}/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

    if not user_info:
        return RedirectResponse(url=f"{frontend_url}/register?error=Google+login+failed")

    email = user_info["email"]
    domain = email.split("@")[-1].lower()
    if domain != ALLOWED_EMAIL_DOMAIN.lower():
        return RedirectResponse(
            url=f"{frontend_url}/register?error=Only+{ALLOWED_EMAIL_DOMAIN}+emails+are+allowed"
        )

    username = email.split("@")[0]
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(username=username, email=email, hashed_password=pwd_context.hash("google_oauth_secret"))
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = create_access_token({"sub": user.username})
    return RedirectResponse(url=f"{frontend_url}?token={jwt_token}")

# -------------------------
# Serve React App
# -------------------------
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Catch-all route to serve React app for client-side routing"""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "build")

    # If static files exist, serve the React app
    if os.path.exists(static_dir):
        file_path = os.path.join(static_dir, full_path)

        # If specific file exists, serve it
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Otherwise serve index.html for client-side routing
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)

    # Fallback if no static files
    raise HTTPException(status_code=404, detail="Not found")
