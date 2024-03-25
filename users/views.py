from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from django.conf import settings

from .serializers import *

@api_view(['GET'])
def home(request):
    return Response({"message": "Server is up and running"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def user_registration(request):
    """creating new user"""
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        """This is the simple login view expect email password and send the token"""
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            current_time = datetime.now()

            response.data["access_token_expiry"] = (current_time + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]).strftime("%Y-%m-%d %H:%M:%S")
            response.data["refresh_token_expiry"] = (current_time + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]).strftime("%Y-%m-%d %H:%M:%S")

        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """This is the simple renewel token view ask for refresh token and send new token"""

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            current_time = datetime.now()

            response.data["access_token_expiry"] = (current_time + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]).strftime("%Y-%m-%d %H:%M:%S")
            response.data["refresh_token_expiry"] = (current_time + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]).strftime("%Y-%m-%d %H:%M:%S")

        return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    serializer = UserMeSerializer(user) 
    return Response(serializer.data, status=status.HTTP_200_OK)