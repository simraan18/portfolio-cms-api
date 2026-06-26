from pydantic import BaseModel

from src.schemas.card_category import CardCategoryResponse

class Card(BaseModel):
    title: str
    description: str
    category_id: str
    slug: str

class CardWithCardId(Card):
    id: str

class CardResponse(Card):
    id: str
    category: CardCategoryResponse
