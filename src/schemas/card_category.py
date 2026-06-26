from pydantic import BaseModel

class CardCategory(BaseModel):
    name: str
    description: str


class CardCategoryResponse(CardCategory):
    id: str
    slug: str