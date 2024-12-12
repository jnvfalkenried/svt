import datetime
import os

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION = os.getenv("JWT_EXPIRATION")

# OAuth2PasswordBearer provides a way to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Hash the password with bcrypt
def hash_password(password: str) -> str:
    """
    Hash the password using bcrypt.
    
    This function takes a plain-text password, salts it, and hashes it using bcrypt.
    The resulting hashed password is returned as a string.

    Args:
        password (str): The plain-text password to hash.
    
    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Verify the password with bcrypt
def verify_password(password: str, hashed_password: str):
    """
    Verify if the given password matches the stored hashed password using bcrypt.
    
    This function compares a plain-text password with a hashed password to verify if they are the same.
    
    Args:
        password (str): The plain-text password to verify.
        hashed_password (str): The stored hashed password to compare against.
    
    Returns:
        bool: True if the password matches the hash, otherwise False.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# Function to create JWT token
def create_access_token(data: dict):
    """
    Create a JWT token with the provided data.
    
    This function generates a JWT access token containing the provided data and an expiration time.
    
    Args:
        data (dict): The payload data to encode in the JWT token. This typically includes user-specific data.
    
    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=int(JWT_EXPIRATION)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency function to verify JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verify the provided JWT token.
    
    This function decodes and validates the JWT token from the Authorization header.
    If the token is valid and not expired, it returns the decoded payload. 
    If the token is invalid or expired, it raises an HTTPException.
    
    Args:
        token (str): The JWT token to verify. It is extracted from the Authorization header.
    
    Returns:
        dict: The decoded JWT payload.
    
    Raises:
        HTTPException: If the token is invalid or expired, an HTTPException with status 401 is raised.
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
