from config.celery import app
from .models import MobileRecord
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

@app.task
def save_mobile(mobile, ip, agent):
    MobileRecord.objects.create(
        mobile=mobile,
    )

    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    db.logs.insert_one({
        "ip": ip,
        "user_agent": agent,
        "timestamp": timezone.now()
    })
