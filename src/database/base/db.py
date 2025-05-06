from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func, text, types, Table
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, mapped_column, relationships
from sqlalchemy.sql.schema import Column

import uuid
from datetime import datetime, date
from typing import List, Union

db = SQLAlchemy()

class UUIDMixin:
    """Adds a primary key with uuid to child classes."""

    __primary_key_field__ = "id"

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("uuid_generate_v4()"),  # use what you have on your server
    )


class SerializationMixin:
    """Provides serialization capabilities to child classes, subclass must inherit from db.Model"""

    @property
    def _table(self) -> Table:
        raise NotImplementedError

    @classmethod
    def serialize(
        cls,
        data: Union[List["SerializationMixin"], "SerializationMixin"],
        *,
        columns=None,
        relation_serialize_params=None,
    ) -> Union[List[dict], dict]:
        kwargs = {"columns": columns, "relation_serialize_params": relation_serialize_params}
        if isinstance(data, list):
            return [obj.to_dict(**kwargs) for obj in data]

        return data.to_dict(**kwargs)

    def to_dict(self, columns=None, relation_serialize_params=None):
        """
        Convert a SQLAlchemy model object to a dictionary.
        """
        result = {}
        relation_serialize_params = relation_serialize_params or {}
        # Iterate through the columns of the model
        if not columns:
            columns = self._table.columns
        for column in columns:
            is_column = isinstance(column, Column)
            is_relation = False
            if hasattr(column, "prop"):
                is_relation = isinstance(column.prop, relationships.Relationship)

            # Extract the column name and value
            if not is_column and is_relation:
                column_name = column.prop.key
                serialization_params = relation_serialize_params.get(column_name)
                if not serialization_params:
                    continue

                obj: "SerializationMixin" = getattr(self, column.prop.key)
                column_value = obj.to_dict(**serialization_params) if obj else None
            else:
                column_name = column.name
                column_value = self._get_value(column_name)

            # Add the column and value to the dictionary
            result[column_name] = column_value

        return result

    def _get_value(self, column_name: str):
        column_value = getattr(self, column_name)

        # Convert any datetime objects to string representation
        if isinstance(column_value, (datetime, date)):
            return column_value.isoformat()

        if isinstance(column_value, uuid.UUID):
            return str(column_value)

        if hasattr(column_value, "_value_"):  # Check if it's an Enum instance
            return column_value.value

        return column_value


class DBSessionMixin:
    """Base class for database operations"""

    @classmethod
    def commit(cls):
        db.session.commit()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            self.commit()

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class TimestampMixin:
    """records creation & update timestamp on objects of child classes."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

@as_declarative()
class BaseModel(UUIDMixin, SerializationMixin, TimestampMixin, DBSessionMixin, db.Model):
    """Base model class combining UUID, serialization and database operations"""
    
    __abstract__ = True
    
    @property
    def _table(self) -> Table:
        return self.__table__

