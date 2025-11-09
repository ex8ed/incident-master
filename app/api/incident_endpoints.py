# -*- coding: UTF-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.core.database import get_db
from app.models.incident_models import StatusEnum
from app.schemas.incident_scheme import IncidentCreate, IncidentUpdate, IncidentResponse
from app.services.incident_service import IncidentService


router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", 
            response_model=IncidentResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Создать инцидент",
            description="Создание нового инцидента")
async def create_incident(incident: IncidentCreate,
                          db: AsyncSession = Depends(get_db)):
    service = IncidentService(db)
    return await service.create_incident(incident)


@router.get("/",
            response_model=List[IncidentResponse],
            summary="Получить список инцидентов",
            description="Получить список всех инцидентов с возможностью фильтрации по статусу и пагинацией")
async def get_incidents(status: Optional[StatusEnum] = Query(None, description="Фильтр по статусу"),
                        skip: int = Query(0, ge=0),
                        limit: int = Query(100, ge=1, le=1000),
                        db: AsyncSession = Depends(get_db)):
    service = IncidentService(db)
    return await service.get_incidents(status=status, skip=skip, limit=limit)


@router.patch("/{incident_id}",
              response_model=IncidentResponse,
              summary="Обновить статус инцидента",
              description="Обновление статуса инцидента по ID")
async def update_incident_status(incident_id: int,
                                 incident_update: IncidentUpdate,
                                 db: AsyncSession = Depends(get_db)):
    service = IncidentService(db)

    updated_incident = await service.update_incident_status(incident_id, 
                                                            incident_update.status)
    
    if not updated_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found")
    
    return updated_incident


@router.get("/{incident_id}",
            response_model=IncidentResponse,
            summary="Получить инцидент по ID",
            description="Получение информации о конкретном инциденте")
async def get_incident(incident_id: int,
                       db: AsyncSession = Depends(get_db)):
    service = IncidentService(db)
    incident = await service.get_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found")
    return incident
