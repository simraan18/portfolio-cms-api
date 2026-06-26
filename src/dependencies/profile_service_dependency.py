from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.services.profile_service import ProfileService
from src.core.database import get_db

async def get_profile_service(db: AsyncIOMotorDatabase = Depends(get_db)):
    return ProfileService(db)