import os
from dotenv import load_dotenv

load_dotenv()  


class Config:
    DEBUG = os.getenv("DEBUG")
    FLASK_DEBUG = 1
    FLASK_ENV = os.getenv("FLASK_ENV")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")  # Default secret key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Secret key for tokens
    # SMTP_SERVER = "localhost"
    # SMTP_PORT = 1025
    # SMTP_USE_TLS = False
    # SMTP_USE_SSL = False
    # SMTP_USERNAME = None
    # SMTP_PASSWORD = None
    # SMTP_DEBUG = True
    # FRONTEND_URL = "https://google.com"
    # SMTP_DEFAULT_SENDER = "testsender@yahoo.com"
    # CLOUD_NAME = os.getenv("CLOUD_NAME")
    # CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
    # CLOUD_API_SECRET_KEY = os.getenv("CLOUD_API_SECRET_KEY")