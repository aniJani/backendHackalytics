from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
db = None


async def init_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DBNAME]
    print("Connected to MongoDB Atlas")


def get_db():
    return db
