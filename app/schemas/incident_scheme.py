# -*- coding: UTF-8 -*-
from pydantic import BaseModel
from datetime import datetime
from app.models.incident_models import SourceEnum, StatusEnum


class IncidentBase(BaseModel):
    description: str
    source: SourceEnum

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: StatusEnum

class IncidentResponse(IncidentBase):
    id: int
    status: StatusEnum
    created_at: datetime

    class Config:
        from_attributes = True
