from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "worker"
