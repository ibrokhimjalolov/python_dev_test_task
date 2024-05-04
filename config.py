from dotenv import load_dotenv
from os import getenv

load_dotenv()


TOKEN = getenv("TOKEN")
MONGO_HOST = getenv("MONGO_HOST", "localhost")
MONGO_PORT = getenv("MONGO_PORT", "27017")
