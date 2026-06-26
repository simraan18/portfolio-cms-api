from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.database import get_db
from src.services.card_categrory_service import CardCategoryService

async def get_card_category_service(db: AsyncIOMotorDatabase = Depends(get_db)):
    return CardCategoryService(db)
