# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "0") == "1"
    # pool settings (optional)
    SQLALCHEMY_POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", 10))
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", 20))

class ProdConfig(BaseConfig):
    DEBUG = False
    ENV = "production"

    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", "5432")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class DevConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    
    # Use same env vars for RDS or a local DB URL if provided
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

config = {
    "production": ProdConfig,
    "development": DevConfig,
    "default": DevConfig,
}
