import logging
from datetime import datetime
from pymongo import MongoClient
from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    """
    Middleware to log all HTTP requests to MongoDB.
    Logs path, method, IP, user agent, and timestamp.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            self.client = MongoClient(settings.MONGO_URI)
            db_name = settings.MONGO_DB
            if not db_name:
                raise ValueError("MONGO_DB is not set")
            self.db = self.client[db_name]
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            self.client = None
            self.db = None

    def __call__(self, request):
        response = self.get_response(request)

        if self.db is not None:
            try:
                ip = request.META.get("REMOTE_ADDR") or request.META.get(
                    "HTTP_X_FORWARDED_FOR", ""
                ).split(",")[0].strip()
                
                self.db.requests.insert_one({
                    "path": request.path,
                    "method": request.method,
                    "ip": ip,
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                    "timestamp": datetime.utcnow(),
                    "status_code": response.status_code,
                })
            except Exception as e:
                logger.error(f"Failed to log request to MongoDB: {str(e)}")

        return response
