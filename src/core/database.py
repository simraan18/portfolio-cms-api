import certifi

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config.config import settings

class Database:
    
    def __init__(self):
        self.client = None
        self.db = None
    
    async def connect(self, url: str, db_name: str):
        self.client = AsyncIOMotorClient(
            url,
            tls=True,
            tlsCAFile=certifi.where()
        )
        self.db = self.client[db_name]

    async def disconnect(self):
        if self.client:
            self.client.close()

database = Database()

async def connect_db():
    try:
        await database.connect(
            settings.database_url,
            settings.database_name
        )
        print("✅ Database connected!")
    except Exception as e:
        print(e)

async def close_db():
    await database.disconnect()

async def get_db():
    yield database.db

async def create_index_card_category_slug(db: AsyncIOMotorDatabase):
    await db.cardCategories.create_index("slug", unique=True)

async def create_index_user_name(db: AsyncIOMotorDatabase):
    await db.users.create_index("username", unique=True)