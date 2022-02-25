from rest_framework import permissions
from api_yamdb.settings import STAFF_ROLES, ADMIN


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    message = "У Вас не достаточно прав, обратитесь к администратору."

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in STAFF_ROLES
                or obj.author == request.user
                or request.user.is_superuser
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == ADMIN)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.role == ADMIN)


class IsAdmin(permissions.BasePermission):
    message = "У Вас не достаточно прав, обратитесь к администратору."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.role == ADMIN
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_superuser
                or request.user.role == ADMIN
                or request.user == obj)
