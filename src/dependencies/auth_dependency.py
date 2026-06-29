from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from bson import ObjectId
from cryptography.fernet import Fernet, InvalidToken

from src.core.database import get_db
from src.services.auth_service import AuthService
from src.utils.jwt import verify_token

async def get_auth_service(db: AsyncIOMotorDatabase = Depends(get_db)):
    return AuthService(db)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        user_id = credentials.credentials.split(".")[0]
        secret_key = credentials.credentials.split(".")[1]

        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        user_token = await db.UserTokens.find_one({"user_id": user_id})
        cipher = Fernet(secret_key)
        decoded_bytes = cipher.decrypt(user_token['hashed_token'])
        cipher._verify_signature
        jwt_token = decoded_bytes.decode('utf-8')
        payload = verify_token(jwt_token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return payload
    except InvalidToken as invalid_token_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except JWTError as jwt_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
