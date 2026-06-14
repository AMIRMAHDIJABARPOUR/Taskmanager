import re
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    identifier = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    @staticmethod
    def is_valid_email(email_str):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email_str) is not None

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        if self.is_valid_email(identifier):
            user = User.objects.filter(email__iexact=identifier).first()
        else:
            user = User.objects.filter(username__iexact=identifier).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed(
                "No active account found with the given credentials",
                code="authentication_failed",
            )

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled", code="user_inactive")

        data = super().get_token(user)
        refresh = self.get_token(user)
        access = refresh.access_token

        refresh["username"] = user.get_username()
        refresh["email"] = getattr(user, "email", "")
        refresh["role"] = getattr(user, "role", "")

        access["username"] = user.get_username()
        access["email"] = getattr(user, "email", "")
        access["role"] = getattr(user, "role", "")

        return {
            "refresh": str(refresh),
            "access": str(access),
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.get_username()
        token["email"] = getattr(user, "email", "")
        token["role"] = getattr(user, "role", "")
        return token


class UserReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "updated_at",
            "role",
        ]
        read_only_fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "updated_at",
            "role",
        ]
