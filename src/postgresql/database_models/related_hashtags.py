from sqlalchemy import ARRAY, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint

from .base import Base


class RelatedHashtags(Base):
    """
    A model that represents the related hashtags in the database.

    The attributes of this model are as follows:

    - hashed_id: A string that represents the hashed version of the related
        hashtag IDs.
    - antecedent_id: A list of strings that represents the IDs of the antecedent
        hashtags.
    - antecedent_title: A list of strings that represents the titles of the
        antecedent hashtags.
    - antecedent_support: A float that represents the support of the antecedent
        hashtags.
    - consequent_id: A list of strings that represents the IDs of the consequent
        hashtags.
    - consequent_title: A list of strings that represents the titles of the
        consequent hashtags.
    - consequent_support: A float that represents the support of the consequent
        hashtags.
    - support: A float that represents the support of the related hashtags.
    - confidence: A float that represents the confidence of the related
        hashtags.
    - lift: A float that represents the lift of the related hashtags.

    The table has the following indexes:

    - idx_antecedent_id_gin: A GIN index on the antecedent_id column.
    - idx_consequent_id_gin: A GIN index on the consequent_id column.
    """

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
        """
        Returns a string representation of the object.

        The string representation includes the values of the antecedent_id,
        antecedent_title, antecedent_support, consequent_id, consequent_title,
        consequent_support, support, confidence, and lift attributes.

        :return: A string representation of the object.
        :rtype: str
        """
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

