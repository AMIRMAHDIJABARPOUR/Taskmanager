from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = "Authentication credentials were not provided"
            return False

        return request.user.role == "admin"


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = "Authentication credentials were not provided"
            return False
        return request.user.role == "worker"
