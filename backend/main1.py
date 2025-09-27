import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

# ----- Settings from ENV -----
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "change-me")
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN", "getcovered.io")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/getcovered_db")

# ----- Database (SQLAlchemy) -----
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="client")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    last_login = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profile")

def init_db():
    Base.metadata.create_all(bind=engine)

# ----- Simple JWT helpers -----
def create_access_token(email: str, role: str, expires_minutes: int = 8*60):
    to_encode = {"sub": email, "role": role, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    encoded = jwt.encode(to_encode, APP_SECRET_KEY, algorithm="HS256")
    return encoded

def decode_access_token(token: str):
    try:
        decoded = jwt.decode(token, APP_SECRET_KEY, algorithms=["HS256"])
        return decoded
    except Exception as e:
        raise

# ----- OAuth (Authlib) -----
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# ----- FastAPI app -----
app = FastAPI(title="GetCovered Demo - FastAPI Backend")
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY)

security = HTTPBearer()

@app.on_event("startup")
def on_startup():
    init_db()
    # seed admin if configured
    if ADMIN_EMAIL:
        db = SessionLocal()
        try:
            admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
            if not admin:
                admin = User(email=ADMIN_EMAIL, first_name="Admin", last_name="User", role="admin")
                db.add(admin)
                db.commit()
        finally:
            db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/auth/login")
async def login(request: Request):
    redirect_uri = GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    # exchange code for token + userinfo
    token = await oauth.google.authorize_access_token(request)
    userinfo = await oauth.google.parse_id_token(request, token)
    email = userinfo.get("email")
    if not email or not email.endswith("@" + ALLOWED_DOMAIN):
        # redirect to frontend unauthorized page
        return RedirectResponse(FRONTEND_URL + "/unauthorized")
    first = userinfo.get("given_name") or ""
    last = userinfo.get("family_name") or ""
    # upsert user
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email, first_name=first or "First", last_name=last or "Last", role="client")
            db.add(user)
            db.commit()
        else:
            user.first_name = first or user.first_name
            user.last_name = last or user.last_name
            user.updated_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()
    # issue JWT and redirect to frontend with token (for demo)
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.email == email).first()
        token_jwt = create_access_token(u.email, u.role)
    finally:
        db.close()
    return RedirectResponse(f"{FRONTEND_URL}/auth?token={token_jwt}")

# ----- Dependencies -----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def admin_required(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user

# ----- User endpoints -----
@app.get("/users/me")
def read_me(current_user=Depends(get_current_user)):
    profile = {
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
        "created_at": current_user.created_at.isoformat(),
    }
    return profile

@app.put("/users/me")
def update_me(payload: dict, db=Depends(get_db), current_user=Depends(get_current_user)):
    current_user.first_name = payload.get("first_name", current_user.first_name)
    current_user.last_name = payload.get("last_name", current_user.last_name)
    db.add(current_user)
    db.commit()
    return {"ok": True, "user": {"email": current_user.email, "first_name": current_user.first_name, "last_name": current_user.last_name}}

# ----- Admin endpoints -----
@app.get("/admin/users")
def list_users(db=Depends(get_db), _=Depends(admin_required)):
    users = db.query(User).all()
    out = []
    for u in users:
        out.append({"email": u.email, "first_name": u.first_name, "last_name": u.last_name, "role": u.role, "created_at": u.created_at.isoformat()})
    return {"count": len(out), "users": out}

@app.get("/admin/overview")
def overview(db=Depends(get_db), _=Depends(admin_required)):
    total = db.query(User).count()
    return {"total_users": total}