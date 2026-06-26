from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Any

from src.schemas.common import ResponseData
from src.schemas.profile import ProfileResponse
from src.utils.normalize_doc import normalize

class ProfileService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_profile(self, payload: dict):
        try:
            results = await self.db.profile.insert_one(
                {
                    "name": payload['name'],
                    "email": payload['email'],
                    "location": payload['location'],
                    "experience": payload['experience'],
                    "education": payload['education'],
                    "visa_status": payload['visa_status'],
                    "about_profile": payload['about_profile'],
                    "skills": payload['skills'],
                    "roles": payload['roles']
                }
            )
            doc = await self.db.profile.find_one({"_id": results.inserted_id})
            doc = normalize(doc)
            res = ProfileResponse(
                id = str(results.inserted_id),
                name = doc["name"],
                email = doc['email'],
                location = doc['location'],
                experience = doc['experience'],
                education = doc['education'],
                visa_status = doc['visa_status'],
                about_profile = doc['about_profile'],
                skills = doc['skills'],
                roles = doc['roles']
            )
            return ResponseData[ProfileResponse](
                data=res,
                status=200,
                message="Profile created successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def get_profile(self):
        try:
            results = await self.db.profile.find().to_list(length=1)
            if len(results) == 0:
                return ResponseData[Any](
                    data={},
                    status=200,
                    message="No data found"
                )
            doc = results[0]
            res = ProfileResponse(
                id = str(doc["_id"]),
                name = doc["name"],
                email = doc['email'],
                location = doc['location'],
                experience = doc['experience'],
                education = doc['education'],
                visa_status = doc['visa_status'] if doc['visa_status'] else None,
                about_profile = doc['about_profile'],
                skills = doc['skills'],
                roles = doc['roles']
            )
            return ResponseData[ProfileResponse](
                data=res,
                status=200,
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def update_profile(self, id: str, payload:dict):
        try:
            results = await self.db.profile.find_one({"_id": ObjectId(id)})
            if not results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
            data = {
                "name": payload['name'],
                "email": payload['email'],
                "location": payload['location'],
                "experience": payload['experience'],
                "education": payload['education'],
                "visa_status": payload['visa_status'],
                "about_profile": payload['about_profile'],
                "skills": payload['skills'],
                "roles": payload['roles']
            }
            await self.db.profile.update_one({"_id": ObjectId(id)}, {"$set": data})
            return ResponseData[Any](
                data={},
                status=200,
                message="Profile updated successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))