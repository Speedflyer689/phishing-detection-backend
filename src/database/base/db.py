from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Session
from sqlalchemy import DateTime, func, text, types
from sqlalchemy.orm import Mapped, mapped_column

import uuid
from datetime import datetime, date
from typing import Dict, Any

db = SQLAlchemy()

class UUIDMixin:
    """Adds a primary key with uuid to child classes."""

    __primary_key_field__ = "id"

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("uuid_generate_v4()"),  # use what you have on your server
    )

class SerializeMixin:
    """Base class for JSON serialization of models"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        """Create model instance from dictionary"""
        return cls(**data)

class DBSessionMixin:
    """Base class for database operations"""

    def save(self, session: Session) -> None:
        """Save instance to database"""
        session.add(self)
        session.flush()

    def delete(self, session: Session) -> None:
        """Delete instance from database"""
        session.delete(self)
        session.flush()

    @classmethod
    def commit(cls, session: Session) -> None:
        """Commit changes to database"""
        session.commit()

class TimestampMixin:
    """records creation & update timestamp on objects of child classes."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

@as_declarative()
class BaseModel(UUIDMixin, SerializeMixin, TimestampMixin, DBSessionMixin, db.Model):
    """Base model class combining UUID, serialization and database operations"""
    
    __abstract__ = True
