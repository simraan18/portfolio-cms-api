from fastapi import APIRouter

route = APIRouter(prefix="/home", tags=["home"])

@route.get("/")
async def getHome():
    return {"message":"Hello, world"}