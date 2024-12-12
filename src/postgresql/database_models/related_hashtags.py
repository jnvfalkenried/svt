from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint

from .base import Base

class RelatedHashtags(Base):
    __tablename__ = "related_hashtags"
    
    antecedent_id: Mapped[str] = mapped_column(String, primary_key=True)
    antecedent_title: Mapped[str] = mapped_column(String)
    antecedent_support: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    consequent_id: Mapped[str] = mapped_column(String, primary_key=True)
    consequent_title: Mapped[str] = mapped_column(String)
    consequent_support: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    support: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    confidence: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    lift: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    
    __table_args__ = (
        PrimaryKeyConstraint("antecedent_id", "consequent_id"),
    )
    
    def __repr__(self):
        return (
            f"RelatedHashtags("
            f"antecedent_id={self.antecedent_id!r}, "
            f"antecedent_title={self.antecedent_title!r}, "
            f"antecedent_support={self.antecedent_support!r}, "
            f"consequent_id={self.consequent_id!r}, "
            f"consequent_title={self.consequent_title!r}, "
            f"consequent_support={self.consequent_support!r}, "
            f"support={self.support!r}, "
            f"confidence={self.confidence!r}, "
            f"lift={self.lift!r}"
            f")"
        )
    