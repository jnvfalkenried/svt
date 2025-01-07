from sqlalchemy import DateTime, Integer, Sequence, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RuleMiningLog(Base):
    """
    Model representing the log for rule mining operations.

    Attributes:
        id (int): The unique identifier for the log entry.
        processed_at (datetime): The timestamp when the log entry was created.
    """

    __tablename__ = "rule_mining_log"

    id: Mapped[int] = mapped_column(
        Integer,
        Sequence("rule_mining_log_id_seq", start=1, increment=1),
        primary_key=True,
    )
    # The timestamp of when the log entry was processed
    processed_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    def __repr__(self) -> str:
        """
        Return a string representation of the RuleMiningLog object.

        Returns:
            str: A string representation of the RuleMiningLog object.
        """
        return (
            f"RuleMiningLog(" f"id={self.id}, " f"processed_at={self.processed_at}" f")"
        )
