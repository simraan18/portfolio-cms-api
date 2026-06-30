from fastapi import APIRouter, Depends

from src.schemas.common import ResponseData, ResponseList
from src.schemas.card import CardResponse, Card, CardWithCardId
from src.services.card_service import CardService
from src.dependencies.card_service_dependency import get_card_service
from src.dependencies.auth_dependency import get_current_user

route = APIRouter(prefix="/card", tags=["card"])

@route.post("", response_model=ResponseData[CardWithCardId])
async def create_card(payload: Card, service: CardService = Depends(get_card_service), user = Depends(get_current_user)):
    response = await service.create_card(payload.model_dump())
    return response

@route.get("", response_model=ResponseList[CardResponse])
async def get_all_cards(service: CardService = Depends(get_card_service), slug: str = None):
    response = await service.get_all_cards(slug=slug)
    return response