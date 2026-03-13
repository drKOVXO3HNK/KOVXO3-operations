import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "KOVXO3 Operations")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./operations.db")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-prod")
JWT_EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MIN", "720"))
