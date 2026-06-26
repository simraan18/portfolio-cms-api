from fastapi import APIRouter, Depends

from src.services.experience_service import ExperienceService
from src.dependencies.experience_service_dependency import get_experience_service
from src.schemas.common import ResponseList, ResponseData
from src.schemas.experience import ExperienceResponse, Experience

route = APIRouter(prefix="/experience", tags=["experience"])

@route.get("", response_model=ResponseList[ExperienceResponse])
async def get_all_experience(service: ExperienceService = Depends(get_experience_service)):
    response = await service.get_all_experience()
    return response

@route.post("", response_model=ResponseData[ExperienceResponse])
async def create_experience(payload: Experience, service: ExperienceService = Depends(get_experience_service)):
    response = await service.create_experience(payload.model_dump())
    return response

@route.put("/{id}", response_model=ResponseData[ExperienceResponse])
async def update_experience(id: str, payload: Experience, service: ExperienceService = Depends(get_experience_service)):
    response = await service.update_experience(id, payload.model_dump())
    return response