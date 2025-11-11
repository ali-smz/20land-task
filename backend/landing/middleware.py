import time
from pymongo import MongoClient
from django.conf import settings

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB]

    def __call__(self, request):
        response = self.get_response(request)

        try:
            self.db.requests.insert_one({
                "path": request.path,
                "method": request.method,
                "ip": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "timestamp": time.time(),
            })
        except:
            pass

        return response
