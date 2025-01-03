from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all database models.

    Contains common column definitions like the "inserted_at" timestamp.
    """
    inserted_at = mapped_column(
        DateTime,
        default=func.now(),
        server_default=func.current_timestamp(),
    )
