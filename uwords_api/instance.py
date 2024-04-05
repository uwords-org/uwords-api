import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# REDIS
REDIS_URL = os.getenv("REDIS_URL")
REDIS_URL_CACHE = os.getenv("REDIS_URL_CACHE")