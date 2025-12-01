# services/payment/app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import PaymentTransaction
from .config import settings

client: AsyncIOMotorClient = None

async def connect_to_mongo():
    """Connect to MongoDB and initialize Beanie."""
    global client
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(database=client[settings.DATABASE_NAME], document_models=[PaymentTransaction])
    print("✅ MongoDB connected and Beanie initialized (payment service).")

async def disconnect_from_mongo():
    """Close Mongo connection."""
    global client
    if client:
        client.close()
        print("🛑 MongoDB connection closed (payment service).")
