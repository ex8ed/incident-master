# -*- coding: UTF-8 -*-
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.incident_models import Incident, StatusEnum
from app.schemas.incident_scheme import IncidentCreate
from app.core.config import setup_logs


logger = setup_logs()


class IncidentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_incident(self, incident_data: IncidentCreate) -> Incident:
        logger.info(f"New incident: source={incident_data.source}")
        try:
            db_incident = Incident(
                description=incident_data.description,
                source=incident_data.source
            )

            self.db.add(db_incident)
            await self.db.commit()
            await self.db.refresh(db_incident)

            logger.info(f"Incident successfully created: id={db_incident.id}")

            return db_incident
        except Exception as e:
            logger.error(f"Failed to create incident: {str(e)}")
            await self.db.rollback()
            raise

    async def get_incidents(self, 
                            status: StatusEnum = None,
                            skip: int = 0, 
                            limit: int = 100) -> list[Incident]:
        query = select(Incident)
        logger.info(f"Fetching incidents: status={status}, skip={skip}, limit={limit}")
        try:
            if status:
                query = query.where(Incident.status == status)

            query = query.offset(skip).limit(limit)
            result = await self.db.execute(query)
            instances = result.scalars().all()

            logger.info(f"Found {len(instances)} incidents!")

            return instances
        except Exception as e:
            logger.error(f"Failed to fetch incidents: {str(e)}")
            raise

    async def get_incident_by_id(self, incident_id: int) -> Incident | None:
        try:
            result = await self.db.execute(
                select(Incident).where(Incident.id == incident_id)
            )

            instance = result.scalar_one_or_none()

            if instance is None:
                logger.warning(f"Incident with id={incident_id} not found")
            return instance
        except Exception as e:
            logger.error(f"Unable to fetch incident with id={incident_id}: {str(e)}")
            raise

    async def update_incident_status(self, 
                                     incident_id: int, 
                                     status: StatusEnum) -> Incident | None:
        logger.info(f"Update incident status: id={incident_id}, new_status={status}")
        try:
            incident = await self.get_incident_by_id(incident_id)

            if not incident:
                return None
            
            incident.status = status
            await self.db.commit()
            await self.db.refresh(incident)
            logger.info(f"Incident {incident_id} status updated: now is {status} ")
            return incident
        except Exception as e:
            logger.error(f"Failed to update incident with id={incident_id}: {str(e)}")
            await self.db.rollback()
            raise
