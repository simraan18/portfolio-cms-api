from pydantic import BaseModel

class UserToken(BaseModel):
    user_id: str
    hashed_token: str
    token_type: str