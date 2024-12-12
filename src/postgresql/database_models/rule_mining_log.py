from sqlalchemy import DateTime, Integer, Sequence, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RuleMiningLog(Base):
    __tablename__ = "rule_mining_log"
    
    id: Mapped[int] = mapped_column(Integer, Sequence("rule_mining_log_id_seq", start=1, increment=1), primary_key=True)
    processed_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    def __repr__(self) -> str:
        return (
            f"RuleMiningLog("
            f"id={self.id}, "
            f"processed_at={self.processed_at}"
            f")"
        )