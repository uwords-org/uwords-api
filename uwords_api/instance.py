import os
import nltk
from dotenv import load_dotenv
from nltk.corpus import stopwords

load_dotenv()

nltk.download('stopwords')

# PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# REDIS
REDIS_URL = os.getenv("REDIS_URL")
REDIS_URL_CACHE = os.getenv("REDIS_URL_CACHE")


STOPWORDS = stopwords.words("russian") + stopwords.words("english")

# MINIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_BUCKET_VOICEOVER = os.getenv("MINIO_BUCKET_VOICEOVER")