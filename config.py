import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PASSWORD_HASH_METHOD = "pbkdf2:sha256"
    SECRET_KEY = os.environ.get("FLASK_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "sqlite:///fisher.db")
    DEBUG = os.environ.get("DEBUG")
    PORT = os.environ.get("PORT")
