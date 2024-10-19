from sqlalchemy import func, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    inserted_at = mapped_column(
        DateTime,
        default=func.now(),
    )
