from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from bson import ObjectId

from src.utils.normalize_doc import normalize
from src.schemas.common import ResponseData, ResponseList
from src.schemas.social_link import SocialLinkResponse

class SocialLinkService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_social_link(self, payload:dict) -> ResponseData[SocialLinkResponse]:
        try:
            data = {
                "title": payload['title'],
                "label": payload['label'],
                "url": payload['url'],
                "platform": payload['platform'],
            }
            results = await self.db.socialLinks.insert_one(data)
            doc = await self.db.socialLinks.find_one({"_id": results.inserted_id})
            doc = normalize(doc)
            return ResponseData[SocialLinkResponse](
                data=doc,
                status=200,
                message="Social link created successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def get_all_links(self) -> ResponseList[SocialLinkResponse]:
        try:
            results = await self.db.socialLinks.find().to_list()
            if len(results) == 0:
                return ResponseList(data=[], status=200, total=0, message="No data found")
            docs = list(map(normalize, results))
            return ResponseList[SocialLinkResponse](data=docs, status=200, total=len(results))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def update_social_link(self, id: str, payload:dict) -> ResponseData[SocialLinkResponse]:

        try:

            doc = await self.db.socialLinks.find_one({"_id": ObjectId(id)})
            if not doc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social link not found")
            
            data = {
                "title": payload['title'],
                "label": payload['label'],
                "url": payload['url'],
                "platform": payload['platform'],
            }
            await self.db.socialLinks.update_one({"_id": ObjectId(id)}, {"$set": data})
            doc = await self.db.socialLinks.find_one({"_id": ObjectId(id)})
            doc = normalize(doc)
            return ResponseData[SocialLinkResponse](
                data=doc,
                status=200,
                message="Social link updated successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))