from rest_framework import permissions


#  TODO Не уверен что этот пермишн нужен, возможно следует удалить
# class IsUserOrAdmin(permissions.BasePermission):
#     message = "У Вас не достаточно прав, обратитесь к администратору."

#     def has_permission(self, request, view):
#         return True

#     def has_object_permission(self, request, view, obj):
#         if (request.method in ['GET', 'PATCH']
#                 and obj.role == request.user.role):
#             return True
#         return obj.role in ['admin', 'superuser']


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    message = "У Вас не достаточно прав, обратитесь к администратору."

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in ['admin', 'superuser', 'moderator']
                or obj.author == request.user
                or request.user.is_superuser
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated 
            and request.user.role in ['admin', 'superuser'])

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.role in ['admin', 'superuser'])

class IsAdmin(permissions.BasePermission):
    message = "У Вас не достаточно прав, обратитесь к администратору."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.role in ['admin', 'superuser']
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_superuser
                or request.user.role in ['admin', 'superuser']
                or request.user == obj)
