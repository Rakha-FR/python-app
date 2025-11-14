import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "postgres_db")
    DB_NAME = os.getenv("DB_NAME", "app_nilai")
    DB_USER = os.getenv("DB_USER", "app_be")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "app#123")
    DB_PORT = int(os.getenv("DB_PORT", 5443))
    
    # Flask config
    DEBUG = bool(os.getenv("DEBUG", "true").lower() == "true")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))