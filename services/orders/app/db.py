from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .config import MONGO_URL, MONGO_DB_NAME
from .models import Order

db_client = None


async def connect_to_mongo():
    """
    initiate the connection to the database
    """
    global db_client
    try:

        db_client = AsyncIOMotorClient(MONGO_URL)


        await init_beanie(
            database=db_client[MONGO_DB_NAME],
            document_models=[Order]
        )
        print("✅ MongoDB connected and Beanie initialized (database.py).")

    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise


async def disconnect_from_mongo():
    """
    close the connection to the database
    """
    global db_client
    if db_client:
        db_client.close()
        print("🔌 MongoDB connection closed.")