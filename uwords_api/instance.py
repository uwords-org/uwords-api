import os
import nltk
from dotenv import load_dotenv
from nltk.corpus import stopwords

load_dotenv()

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
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
