from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.routes.routes import app_routes
from src.core.database import connect_db, close_db, database, create_index_card_category_slug

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()

    db = database.db
    await create_index_card_category_slug(db)

    yield
    await close_db()

# App
app = FastAPI(lifespan=lifespan)


# routes
app.include_router(app_routes, prefix="/api/v1")

# middelwares


# Global Exceptions Handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    if exc.status_code == 404:
        return RedirectResponse(url="/docs")

    return JSONResponse(
        status_code=exc.status_code if exc.status_code is not None else 500,
        content={
            "message": exc
        }
    )