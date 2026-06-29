from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from bson import ObjectId
import json

from src.schemas.common import ResponseList, ResponseData
from src.schemas.experience import ExperienceResponse
from src.utils.normalize_doc import normalize
from src.core.redis import redis
from src.constants.redis_constants import experience_cache_key
from src.config.config import settings


class ExperienceService:

    def __init__(self, db:AsyncIOMotorDatabase):
        self.db = db

    async def get_all_experience(self) -> ResponseList[ExperienceResponse]:
        try:
            cached_results = await redis.get(experience_cache_key)
            if cached_results is not None:
                data = json.loads(cached_results)
                return ResponseList[ExperienceResponse](data=data, status=200, total=len(data))
            expereriences = []
            results = await self.db.experiences.find().to_list()
            if len(results) == 0:
                return ResponseList(data=[], status=200, total=0, message="No data found")
            for item in results:
                item['id'] = str(item["_id"])
                del item['_id']
                expereriences.append(item)
            expereriences_cache_str = json.dumps(expereriences)
            await redis.set(
                experience_cache_key,
                expereriences_cache_str,
                settings.cache_expire
            )
            return ResponseList[ExperienceResponse](data=expereriences, status=200, total=len(expereriences))
        except Exception as e:
            raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def create_experience(self,payload: dict) -> ResponseData[ExperienceResponse]:

        try:
            results = await self.db.experiences.insert_one(payload)
            doc = await self.db.experiences.find_one({"_id": results.inserted_id})
            doc = normalize(doc)
            res = ExperienceResponse(
                id = str(results.inserted_id),
                company = doc["company"],
                country = doc['country'],
                endDate = doc['endDate'],
                responsibilities = doc['responsibilities'],
                role = doc['role'],
                startDate = doc['startDate'],
                technologies = doc['technologies'],
                isCurrent = doc['isCurrent']
            )
            # Invalidate cache
            await redis.delete(experience_cache_key)
            return ResponseData[ExperienceResponse](data=res, status=200, message="Experience created successfully")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
        
    async def update_experience(self, id: str, payload:dict) -> ResponseData[ExperienceResponse]:
        try:
            doc = await self.db.experiences.find_one({"_id": ObjectId(id)})
            if not doc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
            await self.db.experiences.update_one({"_id": ObjectId(id)}, {"$set": payload})
            doc = await self.db.experiences.find_one({"_id": ObjectId(id)})
            response = ExperienceResponse(
                id = id,
                company = doc["company"],
                country = doc['country'],
                endDate = doc['endDate'],
                responsibilities = doc['responsibilities'],
                role = doc['role'],
                startDate = doc['startDate'],
                technologies = doc['technologies']
            )
              # Invalidate cache
            await redis.delete(experience_cache_key)
            return ResponseData[ExperienceResponse](data=response, status=200, message="Experience updated successfully")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
