from rest_framework import permissions

from api_yamdb.settings import NOT_ALLOWED_MESSAGE


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    message = NOT_ALLOWED_MESSAGE

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):

    message = NOT_ALLOWED_MESSAGE

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_admin)


class IsAdmin(permissions.BasePermission):

    message = NOT_ALLOWED_MESSAGE

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_admin
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_superuser
                or request.user.is_admin)
