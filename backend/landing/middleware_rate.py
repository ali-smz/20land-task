import time
import logging
import redis
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    r = redis.from_url(settings.CELERY_BROKER_URL)
except Exception as e:
    logger.error(f"Failed to connect to Redis: {str(e)}")
    r = None


class RateLimitMiddleware:
    """
    Rate limiting middleware using Redis.
    Limits requests to 20 per second per IP address.
    """
    
    RATE_LIMIT = 20  # requests per second
    WINDOW = 1  # time window in seconds
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip rate limiting if Redis is not available
        if not r:
            return self.get_response(request)
        
        try:
            ip = request.META.get("REMOTE_ADDR") or request.META.get(
                "HTTP_X_FORWARDED_FOR", ""
            ).split(",")[0].strip()
            
            # Use current second as part of the key
            current_time = int(time.time())
            key = f"rl:{ip}:{current_time}"

            # Increment counter and set expiration
            current = r.incr(key)
            r.expire(key, self.WINDOW)

            if current > self.RATE_LIMIT:
                logger.warning(f"Rate limit exceeded for IP: {ip}")
                return JsonResponse(
                    {"detail": "Too Many Requests", "error": "Rate limit exceeded"},
                    status=429
                )

            return self.get_response(request)
        except Exception as e:
            logger.error(f"Error in rate limiting: {str(e)}")
            # If there's an error, allow the request to pass
            return self.get_response(request)
