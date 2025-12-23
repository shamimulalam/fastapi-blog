from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone  # Add timezone
import hashlib
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Hash a password using SHA256 + bcrypt"""
    prehashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(prehashed)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    prehashed = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(prehashed, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Dictionary containing user data to encode in token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # ✅ Fixed
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # ✅ Fixed

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise
