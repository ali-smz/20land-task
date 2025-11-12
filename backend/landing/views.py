from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MobileSerializer
from .tasks import save_mobile
import logging

logger = logging.getLogger(__name__)


class SubmitView(APIView):
    """
    API endpoint for submitting mobile number.
    Validates mobile number and processes it asynchronously via Celery.
    """
    
    def post(self, request):
        serializer = MobileSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid mobile number", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        mobile = serializer.validated_data['mobile']
        ip = request.META.get("REMOTE_ADDR") or request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0]
        agent = request.META.get("HTTP_USER_AGENT", "")
        
        try:
            save_mobile.delay(mobile, ip, agent)
            return Response({"status": "ok", "message": "Mobile number submitted successfully"})
        except Exception as e:
            logger.error(f"Error submitting mobile number: {str(e)}")
            return Response(
                {"error": "Failed to process request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
