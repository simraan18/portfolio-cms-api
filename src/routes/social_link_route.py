from fastapi import APIRouter, Depends

from src.schemas.common import ResponseData, ResponseList
from src.schemas.social_link import SocialLinkResponse, SocialLinkBase
from src.services.social_link_service import SocialLinkService
from src.dependencies.social_link_service_dependency import get_social_link_service

route = APIRouter(prefix="/social-link", tags=["social-link"])

@route.get("", response_model=ResponseList[SocialLinkResponse])
async def get_all_social_links(service: SocialLinkService = Depends(get_social_link_service)):
    return await service.get_all_links()

@route.post("", response_model=ResponseData[SocialLinkResponse])
async def create_social_link(payload: SocialLinkBase, service:SocialLinkService = Depends(get_social_link_service)):
    return await service.create_social_link(payload.model_dump())

@route.put("/{id}", response_model=ResponseData[SocialLinkResponse])
async def update_social_link(id: str, payload: SocialLinkBase, service: SocialLinkService = Depends(get_social_link_service)):
    return await service.update_social_link(id, payload.model_dump())