from pydantic import BaseModel, EmailStr

class Auth(BaseModel):

    username: EmailStr
    password: str

class Token(BaseModel):
    
    access_token: str
    token_type: str