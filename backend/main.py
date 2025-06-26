from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load .env file from the project root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Get MongoDB credentials from environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
db_name = os.getenv("MONGO_DB_NAME")

# Raise an error if any env variable is missing
if not all([username, password, db_name]):
    raise EnvironmentError("Missing one or more MongoDB credentials in .env file")

# Construct MongoDB URI
uri = f"mongodb+srv://{username}:{password}@{db_name}.ib5vj55.mongodb.net/?retryWrites=true&w=majority&appName={db_name}"

# Initialize FastAPI app
app = FastAPI()

# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB!")
except Exception as e:
    print("❌ Failed to connect to MongoDB:", e)
