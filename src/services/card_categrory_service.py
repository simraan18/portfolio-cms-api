from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from src.schemas.common import ResponseData, ResponseList
from src.schemas.card_category import CardCategoryResponse
from src.utils.normalize_doc import normalize
from src.utils.generate_slug import generate_slug

class CardCategoryService:

    def __init__(self, db:AsyncIOMotorDatabase):
        self.db = db

    async def create_card_category(self,payload: dict) -> ResponseData[CardCategoryResponse]:
        try:
            slug = generate_slug(payload['name'])
            results = await self.db.cardCategories.insert_one(
                {
                    "name": payload['name'],
                    "description": payload['description'],
                    "slug": slug
                }
            )
            doc = await self.db.cardCategories.find_one({"_id": results.inserted_id})
            doc = normalize(doc)
            res = CardCategoryResponse(
                id = str(results.inserted_id),
                name = doc["name"],
                description = doc['description'],
                slug = doc['slug']
            )
            return ResponseData[CardCategoryResponse](data=res, status=200, message="Card category created successfully")
        except DuplicateKeyError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Card category already exists")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)) 
        

    async def get_all_card_category(self) -> ResponseList[CardCategoryResponse]:
        try:
            cardCategories = []
            results = await self.db.cardCategories.find().to_list()
            if len(results) == 0:
                return ResponseList(data=[], status=200, total=0, message="No data found")
            cardCategories = list(map(normalize, results))
            return ResponseList[CardCategoryResponse](data=cardCategories, status=200, total=len(cardCategories))
        except Exception as e:
            raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))