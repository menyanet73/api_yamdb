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
