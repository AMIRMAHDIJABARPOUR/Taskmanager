from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import CustomTokenObtainPairSerializer, UserReadOnlySerializer
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserReadOnlyAPIView(generics.RetrieveAPIView):
    serializer_class = UserReadOnlySerializer
    queryset = User.objects.all()
