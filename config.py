from dotenv import load_dotenv
from os import getenv

load_dotenv()


TOKEN = getenv("TOKEN")
MONGO_URL = getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = getenv("MONGO_DB_NAME", "test")
MONGO_COLLECTION = getenv("MONGO_COLLECTION", "test")
