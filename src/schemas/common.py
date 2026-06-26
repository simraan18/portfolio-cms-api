from pydantic import BaseModel

class ResponseData[T](BaseModel):
    
    data: T
    status: int
    message: str = "OK"


class ResponseList[T](BaseModel):

    data: list[T]
    status: int
    message: str = "OK"
    total: int = 0