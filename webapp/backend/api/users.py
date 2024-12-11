import uuid

from core.auth import create_access_token, hash_password, verify_password
from fastapi import APIRouter, HTTPException
from schemas.request import LoginRequest, UserRequest
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import Users
from postgresql.database_scripts.users import insert_user

router = APIRouter()


@router.post("/api/register")
async def register(user: UserRequest) -> dict[str, str]:
    # Run a query to register a user
    async with session() as s:
        # Check if the user already exists
        result = await s.execute(select(Users).where(Users.username == user.username))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash the password
        user.password = hash_password(user.password)

        try:
            uuid_str = str(uuid.uuid4())
            await insert_user(
                id=uuid_str,
                username=user.username,
                email=user.email,
                password_hash=user.password,
                roles=user.roles,
                session=s,
            )
            await s.commit()
            return {"message": "User registered successfully"}
        except Exception as e:
            print(f"Error in transaction, rolling back: {e}")
            await s.rollback()
            raise HTTPException(status_code=500, detail="Failed to register user")


@router.post("/api/login")
async def login(login_request: LoginRequest) -> dict[str, str]:
    # Run a query to login a user
    async with session() as s:
        # Check if the user exists
        result = await s.execute(
            select(Users).where(Users.username == login_request.username)
        )
        user = result.scalars().first()

        # Verify the user
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Verify the password
        if not verify_password(login_request.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Create JWT token
        access_token = create_access_token(
            data={"username": user.username, "email": user.email, "roles": user.roles}
        )
        return {"access_token": access_token, "token_type": "bearer"}
