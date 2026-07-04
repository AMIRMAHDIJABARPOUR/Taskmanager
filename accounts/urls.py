from django.urls import path, include
from .views import CustomTokenObtainPairView, UserReadOnlyAPIView, CustomTokenVerifyView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
)

urlpatterns = [
    path("auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/jwt/verify/", CustomTokenVerifyView.as_view(), name="jwt-verify"),
    path("auth/jwt/logout/", TokenBlacklistView.as_view(), name="jwt-logout"),
    path("auth/", include("djoser.urls")),
    path(
        "api/user-details/<int:pk>/",
        UserReadOnlyAPIView.as_view(),
        name="accounts-user-details",
    ),
]
