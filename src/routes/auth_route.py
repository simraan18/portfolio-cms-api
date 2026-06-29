from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.services.auth_service import AuthService
from src.dependencies.auth_dependency import get_auth_service
from src.schemas.auth import Auth
from src.schemas.common import ResponseData

route = APIRouter(prefix="/auth", tags=["auth"])

@route.post("/sign-up", response_model=ResponseData[str])
async def sign_up(payload: Auth, service: AuthService = Depends(get_auth_service)):
    return await service.create_user(payload.model_dump())

@route.post("/sign-in")
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    return await service.sign_in(form_data)