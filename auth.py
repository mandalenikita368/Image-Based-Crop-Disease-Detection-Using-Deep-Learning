import bcrypt
from sqlalchemy.orm import Session
from models import User
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_user(db: Session, username: str, email: str, password: str, full_name: str = None):
    """Create a new user"""
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        if existing_user.username == username:
            return None, "Username already exists"
        else:
            return None, "Email already exists"
    
    password_hash = hash_password(password)
    
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user, None

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user"""
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return None, "Invalid username or password"
    
    if not verify_password(password, user.password_hash):
        return None, "Invalid username or password"
    
    return user, None

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()
