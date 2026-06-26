from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.database import get_db
from src.services.experience_service import ExperienceService

async def get_experience_service(db: AsyncIOMotorDatabase = Depends(get_db)):
    return ExperienceService(db)