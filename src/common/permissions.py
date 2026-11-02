from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAnonymousPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsSameUserPermission(BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get("username")
        if not username:
            return False
        return request.user.is_authenticated and request.user.username.lower() == username.lower()


class IsNotSelfPermission(BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get("username")
        if not username:
            return True
        return request.user.is_authenticated and request.user.username.lower() != username.lower()
