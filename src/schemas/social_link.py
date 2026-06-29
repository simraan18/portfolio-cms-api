from pydantic import BaseModel

class SocialLinkBase(BaseModel):
    title: str
    label: str
    url: str
    platform: str

class SocialLinkResponse(SocialLinkBase):
    id: str
