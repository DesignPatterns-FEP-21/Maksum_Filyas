#Цей файл відповідає за управління підключенням до бази даних MongoDB
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.logger import logger

class MongoDB:
    """Клас для управління підключенням до MongoDB."""
    client: AsyncIOMotorClient = None

db_client = MongoDB()

async def get_database():
    """Повертає об'єкт бази даних."""
    if db_client.client is None:
        logger.error("Database client not initialized. Call connect_to_mongo first.")
        return None
    return db_client.client[settings.DB_NAME]

async def connect_to_mongo():
    """Встановлює з'єднання з MongoDB під час старту додатку."""
    logger.info("Connecting to MongoDB...")
    try:
        db_client.client = AsyncIOMotorClient(settings.MONGO_URL)
        # Перевірка з'єднання
        await db_client.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        db_client.client = None


async def close_mongo_connection():
    """Закриває з'єднання з MongoDB під час зупинки додатку."""
    if db_client.client:
        logger.info("Closing MongoDB connection...")
        db_client.client.close()
        logger.info("MongoDB connection closed.")