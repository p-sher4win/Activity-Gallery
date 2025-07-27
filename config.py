import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("FLASK_ENV") == "development"
    MONGO_PASS = os.getenv("MONGO_PASS")
    MONGO_URI = f'mongodb+srv://sher4win:{MONGO_PASS}@cluster0.rqvughq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    CLOUD_NAME = os.getenv("CLOUD_NAME")
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    CLOUDINARY_URL= f'cloudinary://{API_KEY}:{API_SECRET}@{CLOUD_NAME}'