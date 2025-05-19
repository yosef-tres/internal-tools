"""Database models for FDC."""

from datetime import datetime
from datetime import timezone
from typing import List, Optional
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .session import Base

class Collection(Base):
    """Collection model represents a top-level collection of data."""
    
    __tablename__ = "collection"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # One-to-many relationship with CollectionPart
    parts: Mapped[List["CollectionPart"]] = relationship(
        "CollectionPart", 
        back_populates="collection",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Collection(id={self.id}, name={self.name})>"


class CollectionPart(Base):
    """CollectionPart model represents a part of a collection."""
    
    __tablename__ = "collection_part"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string for flexible metadata
    order: Mapped[int] = mapped_column(Integer, default=0)  # For ordered parts
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Many-to-one relationship with Collection
    collection: Mapped[Optional["Collection"]] = relationship(
        "Collection", 
        back_populates="parts"
    )
    
    def __repr__(self) -> str:
        return f"<CollectionPart(id={self.id}, name={self.name}, collection_id={self.collection_id})>"
