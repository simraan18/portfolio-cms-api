from fastapi import HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

from src.config.config import settings
from src.schemas.common import ResponseData


class AuthService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')

    
    async def create_user(self, payload: dict):
        try:
            hashed_password = self.bcrypt_context.hash(payload['password'])
            data = {
                "password": hashed_password,
                "username": payload['username'],   
            }
            results = await self.db.users.insert_one(data)
            return ResponseData[str](data=str(results.inserted_id), status=status.HTTP_201_CREATED, message="User created successfully")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def sign_in(self, payload: dict = Depends()):
        try:
            user = await self.db.users.find_one({"username": payload['username']})
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication credentials not found")
            if not self.bcrypt_context.verify(payload['password'], user['password']):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication credentials not found")
            jwt_payload = {
                "sub": user['username'],
                "id": str(user['_id']),
                "exp": datetime.now() + timedelta(days=7)
            }
            access_token = AuthService.create_access_token(jwt_payload)
            token = await AuthService.securely_store_token(access_token, user, self.db)
            return ResponseData[dict](data={"access_token": token}, status=status.HTTP_200_OK, message="User signed in successfully")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod    
    def create_access_token(data: dict):
        try:
            to_encode = data.copy()
            return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod    
    def encode_token(token: str, secret_key: bytes):
        cipher = Fernet(secret_key)
        text_bytes = token.encode('utf-8')
        encoded_bytes = cipher.encrypt(text_bytes)
        encoded_text = encoded_bytes.decode('utf-8')
        return encoded_text

    @staticmethod    
    async def securely_store_token(token: str, user: dict, db: AsyncIOMotorDatabase):
        secret_key = Fernet.generate_key()
        encoded_text = AuthService.encode_token(token, secret_key)
        await db.UserTokens.delete_one({"user_id": str(user['_id'])})
        await db.UserTokens.insert_one({
            "user_id": str(user['_id']),
            "hashed_token": encoded_text,
            "token_type": "jwt",
        })
        return f"{str(user['_id'])}.{secret_key.decode('utf-8')}"