from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
ai_logs = db.ai_generation_logs
