import uuid

from sqlalchemy import Column, Date, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, ExcludeConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative Base class for SQLAlchemy models."""
    pass

class LegalArticleVersion(Base):
    """
    SQLAlchemy model representing a specific version of a legal article.
    Stores metadata, hierarchy, content in Arabic and optionally French,
    and validity dates for temporal auditing.
    """
    __tablename__ = 'legal_article_version'

    version_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    article_id = Column(String(100), nullable=False, index=True)
    code_id = Column(String(50), nullable=False, index=True)
    article_number = Column(String(50), nullable=False)
    hierarchy_path = Column(Text, nullable=False)  # Chapter/section tree representation
    text_ar = Column(Text, nullable=False)
    text_fr = Column(Text, nullable=True)  # French version of the law if available
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="active")  # active, superseded, repealed
    source_ref = Column(JSONB, nullable=False)  # Metadata mapping page/coords/run IDs
    created_by_op = Column(String(100), nullable=True)  # Run ID or operator context

    __table_args__ = (
        Index('idx_code_article_valid', 'code_id', 'article_number', 'valid_from'),
        Index('idx_article_valid', 'article_id', 'valid_from'),
        Index('idx_source_ref', 'source_ref', postgresql_using='gin'),
        ExcludeConstraint(
            ('article_id', '='),
            (func.daterange(valid_from, valid_to), '&&'),
            name='excl_article_valid_dates'
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<LegalArticleVersion(version_id={self.version_id}, "
            f"article_id={self.article_id}, code_id={self.code_id}, "
            f"valid_from={self.valid_from})>"
        )

