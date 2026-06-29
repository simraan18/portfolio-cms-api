from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.database import get_db
from src.services.social_link_service import SocialLinkService

async def get_social_link_service(db: AsyncIOMotorDatabase = Depends(get_db)):
    return SocialLinkService(db)
