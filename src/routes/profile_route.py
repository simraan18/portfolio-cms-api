from fastapi import APIRouter, Depends
from typing import Any

from src.schemas.common import ResponseData
from src.schemas.profile import ProfileResponse, ProfileBase
from src.services.profile_service import ProfileService
from src.dependencies.profile_service_dependency import get_profile_service
from src.dependencies.auth_dependency import get_current_user

route = APIRouter(prefix="/profile", tags=["profile"])


@route.post("", response_model=ResponseData[ProfileResponse])
async def create_profile(profile: ProfileBase ,service: ProfileService = Depends(get_profile_service), user = Depends(get_current_user)):
    response = await service.create_profile(profile.model_dump())
    return response

@route.get("", response_model=ResponseData[Any])
async def get_profile(service: ProfileService = Depends(get_profile_service)):
    response = await service.get_profile()
    return response

@route.put("/{id}", response_model=ResponseData[Any])
async def update_profile(id: str, profile: ProfileBase, service: ProfileService = Depends(get_profile_service), user = Depends(get_current_user)):
    response = await service.update_profile(id, profile.model_dump())
    return response