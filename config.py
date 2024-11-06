from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///note_book.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
