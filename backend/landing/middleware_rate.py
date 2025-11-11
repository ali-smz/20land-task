import time
import redis
from django.http import JsonResponse
from django.conf import settings

r = redis.from_url(settings.CELERY_BROKER_URL)

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        key = f"rl:{ip}:{int(time.time())}"

        current = r.incr(key)
        r.expire(key, 1)

        if current > 20:  # 20 req/sec
            return JsonResponse({"detail": "Too Many Requests"}, status=429)

        return self.get_response(request)
