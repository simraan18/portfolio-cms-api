from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

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
@app.exception_handler(ValueError)
async def value_error_handler(
    request: Request,
    exc: ValueError
):
    return JSONResponse(
        status_code=400,
        content={
            "message": str(exc)
        }
    )