from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class PostAPIView(APIView):
    """
    A simple APIView that supports GET and POST requests.
    - GET returns a welcome message.
    - POST echoes back the provided JSON payload with a message.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = {
            "message": "GET request successful",
            "info": "Use POST to echo your payload"
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        payload = request.data
        data = {
            "message": "POST request successful",
            "payload": payload
        }
        return Response(data, status=status.HTTP_201_CREATED)
