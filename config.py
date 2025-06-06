import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PASSWORD_HASH_METHOD = "pbkdf2:sha256"
    SALT_LENGTH = 4
    SECRET_KEY = os.environ.get("FLASK_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "sqlite:///fisher.db")
    APP_DEBUG = os.environ.get("DEBUG")
    PORT = os.environ.get("PORT")
    # 分页配置
    ITEMS_PER_PAGE = 10  # 默认每页显示数量
