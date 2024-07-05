from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from app.core.config import settings
import certifi

# MongoDB connection URI
MONGO_URI = f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_DB}.akodian.mongodb.net/?appName=SiteCurve"

print(MONGO_URI)

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.get_database("sitecurve")

async def get_mongo_db():
    try:
        # Check if the connection is established
        await client.admin.command('ping')
        print("MongoDB connected successfully")
    except ConnectionFailure:
        print("MongoDB connection failed")
        raise ConnectionFailure("MongoDB connection failed")

    return db
