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
    Hashes a given password with a random salt.

    :param password: The password to be hashed.
    :return: The hashed password as a string.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Verify the password with bcrypt
def verify_password(password: str, hashed_password: str):
    """
    Verifies a given password against a hashed password.

    :param password: The password to be verified.
    :param hashed_password: The hashed password to compare against.
    :return: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# Function to create JWT token
def create_access_token(data: dict):
    """
    Creates a JWT token with the given data and expiration time.

    :param data: Data to be encoded in the JWT token.
    :return: The encoded JWT token as a string.
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
    Verifies a JWT token and returns the decoded payload.

    :param token: The JWT token to be verified.
    :return: The decoded payload as a dictionary.
    :raises HTTPException: If the token is invalid or expired.
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
