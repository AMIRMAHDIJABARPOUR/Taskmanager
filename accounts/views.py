from django.contrib.auth import get_user_model
from .serializers import CustomTokenObtainPairSerializer, UserReadOnlySerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.response import Response

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserReadOnlyAPIView(generics.RetrieveAPIView):
    serializer_class = UserReadOnlySerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({"message": "Token is valid"})
