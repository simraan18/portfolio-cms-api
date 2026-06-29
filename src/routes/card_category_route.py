from fastapi import APIRouter, Depends


from src.schemas.common import ResponseData, ResponseList
from src.schemas.card_category import CardCategoryResponse, CardCategory 
from src.services.card_categrory_service import CardCategoryService
from src.dependencies.card_category_service_dependency import get_card_category_service
from src.dependencies.auth_dependency import get_current_user

route = APIRouter(prefix="/card-category", tags=["card-category"])


@route.post("", response_model=ResponseData[CardCategoryResponse])
async def create_card_category(payload: CardCategory, service: CardCategoryService = Depends(get_card_category_service)):
    response = await service.create_card_category(payload.model_dump())
    return response

@route.get("", response_model=ResponseList[CardCategoryResponse])
async def get_all_card_category(service: CardCategoryService = Depends(get_card_category_service), user = Depends(get_current_user)):
    response = await service.get_all_card_category()
    return response