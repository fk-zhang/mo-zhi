"""MongoDB connection management."""
from typing import Optional
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from .config import settings

logger = logging.getLogger(__name__)

class MongoDBManager:
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        """Get or create a MongoDB client instance with connection pooling.
        
        Returns:
            AsyncIOMotorClient: MongoDB client instance
        """
        if cls._client is None:
            try:
                cls._client = AsyncIOMotorClient(
                    settings.mongo_uri,
                    **settings.mongo_connection_options
                )
                logger.info("MongoDB client initialized")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
        return cls._client

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get the database instance.
        
        Returns:
            AsyncIOMotorDatabase: Database instance
        """
        if cls._db is None:
            client = cls.get_client()
            cls._db = client[settings.mongo_db]
        return cls._db

    @classmethod
    async def close_connection(cls) -> None:
        """Close the MongoDB connection."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")

    @classmethod
    async def ping(cls) -> bool:
        """Ping the MongoDB server to check the connection.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            client = cls.get_client()
            await client.admin.command('ping')
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB connection failed: {e}")
            return False

# Dependency to get MongoDB database instance
async def get_mongodb() -> AsyncIOMotorDatabase:
    """FastAPI dependency to get MongoDB database instance.
    
    Example:
        @router.get("/example")
        async def example_route(db: AsyncIOMotorDatabase = Depends(get_mongodb)):
            # Use the database
            result = await db.your_collection.find_one({"key": "value"})
            return result
    """
    return MongoDBManager.get_db()
