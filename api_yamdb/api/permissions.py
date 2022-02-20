from rest_framework import permissions


class IsUserOrAdmin(permissions.BasePermission):
    message = "У Вас не достаточно прав, обратитесь к администратору."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if (request.method in ['GET', 'PATCH']
                and obj.role == request.user.role):
            return True
        return obj.role in ['admin', 'superuser']


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in ['admin', 'superuser', 'moderator']
                or obj.author == request.user
                )
