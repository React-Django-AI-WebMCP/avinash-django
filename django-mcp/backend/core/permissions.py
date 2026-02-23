from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Object-level permission: only allow the owner of an object to access it.
    The model must expose an `owner` FK to the user model.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrReadOnly(BasePermission):
    """Read-only for all; write only for the owner."""

    def has_object_permission(self, request, view, obj):
        from rest_framework.permissions import SAFE_METHODS

        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAdminOrReadOnly(BasePermission):
    """Read-only for authenticated users; write for admins."""

    def has_permission(self, request, view):
        from rest_framework.permissions import SAFE_METHODS

        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff
