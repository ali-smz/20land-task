import logging
from datetime import datetime
from pymongo import MongoClient
from django.db import IntegrityError
from django.conf import settings
from config.celery import app
from .models import MobileRecord

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3)
def save_mobile(self, mobile, ip, agent):
    """
    Celery task to save mobile number to PostgreSQL and log to MongoDB.
    
    Args:
        mobile: Mobile number string
        ip: IP address of the client
        agent: User agent string
    """
    try:
        # Save to PostgreSQL (handle duplicate mobile numbers)
        mobile_record, created = MobileRecord.objects.get_or_create(mobile=mobile)
        if created:
            logger.info(f"Mobile number {mobile} saved to database")
        else:
            logger.info(f"Mobile number {mobile} already exists in database")
        
        # Log to MongoDB (always log, even if duplicate)
        try:
            client = MongoClient(settings.MONGO_URI)
            db_name = settings.MONGO_DB
            if not db_name:
                logger.warning("MONGO_DB is not set!")
                return 

            db = client[db_name]
            db.logs.insert_one({
                "ip": ip,
                "user_agent": agent,
                "timestamp": datetime.utcnow(),
                "is_duplicate": not created,
            })
            client.close()

            logger.info(f"Mobile number {mobile} logged to MongoDB")
        except Exception as e:
            logger.error(f"Failed to log to MongoDB: {str(e)}")
            # Don't fail the task if MongoDB logging fails
            
    except IntegrityError as e:
        logger.warning(f"Duplicate mobile number {mobile}: {str(e)}")
        # Don't retry on integrity errors (duplicate)
    except Exception as e:
        logger.error(f"Error saving mobile number {mobile}: {str(e)}")
        # Retry the task if it fails (max 3 times)
        raise self.retry(exc=e, countdown=60)
