from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MobileSerializer
from .tasks import save_mobile

class SubmitView(APIView):
    def post(self, request):
        ser = MobileSerializer(data=request.data)

        if ser.is_valid():
            mobile = ser.validated_data["mobile"]
            ip = request.META.get("REMOTE_ADDR")
            agent = request.META.get("HTTP_USER_AGENT")

            save_mobile.delay(mobile, ip, agent)

            return Response({"status": "ok", "msg": "saved"})

        return Response(ser.errors, status=400)
