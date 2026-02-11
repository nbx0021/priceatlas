import os

class Config:
    DEBUG = True
    DB_URL = os.getenv("DB_URL", "sqlite:///priceatlas.db")
    FOREX_API = os.getenv("FOREX_API", "")
