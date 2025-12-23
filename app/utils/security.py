from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using SHA256 + bcrypt
    SHA256 ensures we stay within bcrypt's 72-byte limit
    """
    # Pre-hash with SHA256 to handle any length password
    prehashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # Then hash with bcrypt
    return pwd_context.hash(prehashed)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    # Pre-hash with SHA256
    prehashed = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    # Then verify with bcrypt
    return pwd_context.verify(prehashed, hashed_password)
