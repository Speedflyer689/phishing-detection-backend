from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum

from datetime import datetime
from library.datetime import get_current_utc_time
from database.base.db import BaseModel
from database.base.enums import PhishingType

class PhishingIncident(BaseModel):
    __tablename__ = "phishing_incidents"

    content: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[PhishingType] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(default=1)
