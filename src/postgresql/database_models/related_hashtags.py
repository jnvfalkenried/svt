from sqlalchemy import ARRAY, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint

from .base import Base


class RelatedHashtags(Base):
    __tablename__ = "related_hashtags"

    hashed_id: Mapped[str] = mapped_column(String, primary_key=True)
    antecedent_id: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    antecedent_title: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    antecedent_support: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    consequent_id: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    consequent_title: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    consequent_support: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    support: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    confidence: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))
    lift: Mapped[float] = mapped_column(Numeric(precision=7, scale=5))

    __table_args__ = (
        Index("idx_antecedent_id_gin", "antecedent_id", postgresql_using="gin"),
        Index("idx_consequent_id_gin", "consequent_id", postgresql_using="gin"),
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
