from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import save_mobile

class SubmitView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        ip = request.META.get("REMOTE_ADDR")
        agent = request.META.get("HTTP_USER_AGENT")

        save_mobile.delay(mobile, ip, agent)

        return Response({"status": "ok"})
