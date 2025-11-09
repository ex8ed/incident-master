# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum


Base = declarative_base()


class StatusEnum(str, enum.Enum):
    OPEN = "open"
    IN_PROCESS = "in_process"
    RESOLVED = "resolved"
    CLOSED = "closed"

class SourceEnum(str, enum.Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.OPEN, nullable=False)
    source = Column(Enum(SourceEnum), nullable=False)
