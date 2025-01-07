import uuid
from typing import List

from sqlalchemy import Boolean, Index, String
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Users(Base):
    """
    Represents a user in the database.

    Attributes:
        id (UUID): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user, must be unique.
        password_hash (str): The hashed password of the user.
        active (bool): Whether the user account is active.
        roles (List[str]): The roles assigned to the user.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    roles: Mapped[List[str]] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        # Create an index on the email column for faster lookups.
        Index("users_email", "email"),
    )
