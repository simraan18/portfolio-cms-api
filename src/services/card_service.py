from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from bson import ObjectId
from typing import Optional

from src.schemas.card import CardResponse, CardWithCardId
from src.schemas.common import ResponseData, ResponseList
from src.utils.aggregations import card_with_category_lookup
from src.schemas.card_category import CardCategoryResponse

class CardService:

    def __init__(self, db:AsyncIOMotorDatabase):
        self.db = db

    async def create_card(self, payload: dict) -> ResponseData[CardWithCardId]:
        try:
            results = await self.db.cards.insert_one(
                {
                    "title": payload['title'],
                    "description": payload['description'],
                    "category_id": ObjectId(payload['category_id']),
                    "slug": payload['slug']
                }
            )
            doc = await self.db.cards.find_one({"_id": results.inserted_id})
            res = {
                "id": str(results.inserted_id),
                "title": doc["title"],
                "description": doc['description'],
                "category_id": str(doc['category_id']),
                "slug": doc['slug']
            }
            return ResponseData[CardWithCardId](data=res, status=200, message="Card created successfully")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def get_all_cards(self, slug:Optional[str]) -> ResponseList[CardResponse]:
        try:
            results = None
            if slug is not None:
                find_by_slug_pipline = [
                    {
                        "$match": {
                            "slug": slug
                        }
                    },
                    *card_with_category_lookup
                ]
                results = await self.db.cards.aggregate(find_by_slug_pipline).to_list()
            else:
                results = await self.db.cards.aggregate(card_with_category_lookup).to_list()
            if len(results) == 0:
                return ResponseList(data=[], status=200, total=0, message="No data found")
            
            map_card = lambda x: CardResponse(
                id = str(x["_id"]),
                category = CardCategoryResponse(
                    id = str(x['category']["_id"]),
                    name = x['category']["name"],
                    description = x['category']["description"],
                    slug = x['category']["slug"]
                ),
                category_id = str(x["category_id"]),
                title = x["title"],
                description = x["description"],
                slug = x["slug"],
            )
            cards = list(map(map_card, results))
            return ResponseList[CardResponse](data=cards, status=200, total=len(cards))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))