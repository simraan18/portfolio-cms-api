from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.database import get_db
from src.services.card_service import CardService


async def get_card_service(db: AsyncIOMotorDatabase = Depends(get_db)):
    return CardService(db)
