import re
import hashlib
from typing import Tuple
from database import add_user, verify_user

def hash_password(password: str) -> str:
    """Create a SHA-256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """
    Validate password strength:
    - At least 8 characters
    - Contains both letters and numbers
    """
    if len(password) < 8:
        return False
    if not any(c.isalpha() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def signup(email: str, password: str) -> Tuple[bool, str]:
    """Handle user signup"""
    if not validate_email(email):
        return False, "Invalid email format"
    
    if not validate_password(password):
        return False, "Password must be at least 8 characters and contain both letters and numbers"
    
    hashed_password = hash_password(password)
    if add_user(email, hashed_password):
        return True, "Signup successful"
    return False, "Email already exists"

def login(email: str, password: str) -> Tuple[bool, str]:
    """Handle user login"""
    if not validate_email(email):
        return False, "Invalid email format"
    
    hashed_password = hash_password(password)
    if verify_user(email, hashed_password):
        return True, "Login successful"
    return False, "Invalid email or password"
