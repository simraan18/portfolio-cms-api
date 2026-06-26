from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileBase(BaseModel):
    name: str
    email: EmailStr
    location: str
    experience: int
    education: str
    visa_status: Optional[str]
    about_profile: str
    skills: list[str]
    roles: list[str]

class ProfileResponse(ProfileBase):
    id: str