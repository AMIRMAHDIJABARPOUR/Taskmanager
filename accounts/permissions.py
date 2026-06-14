from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserRoleAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == "admin" or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == "admin" or request.user.is_superuser
