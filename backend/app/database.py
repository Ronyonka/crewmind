import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, InvalidName
from urllib.parse import urlparse
import logging
from dotenv import load_dotenv

# Get the root directory path (two levels up from this file)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from the root directory
load_dotenv(os.path.join(ROOT_DIR, ".env"))

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    """Get database instance."""
    return db.database


async def connect_to_mongo():
    """Create database connection."""
    try:
        # Get connection string from environment
        connection_string = os.getenv("MONGO_URI")

        if not connection_string:
            raise ValueError(
                "Missing MongoDB connection string in environment variables"
            )

        # Parse the connection string to get database name
        parsed_uri = urlparse(connection_string)
        db_name = parsed_uri.path.lstrip("/")

        if not db_name or "?" in db_name:
            db_name = os.getenv("MONGO_DB_NAME", "crewmind")  # fallback to default name

        # Create client with database name removed from connection string
        db.client = AsyncIOMotorClient(connection_string)

        # Test connection
        await db.client.admin.command("ping")

        # Set database
        db.database = db.client[db_name]

        logger.info(f"Successfully connected to MongoDB database: {db_name}")

    except (ConnectionFailure, InvalidName) as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection."""
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed")
