# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    MONGO_URI = 'mongodb://localhost:27017/'
    MONGO_DB = 'Hotel_reservation_system'

    # Flask-Mail configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # JWT secret key
    SECRET_KEY = os.getenv('SECRET_KEY', '59a4ecd754c57833ffe61c94a568a390')