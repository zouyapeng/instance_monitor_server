from rest_framework.permissions import BasePermission

class IsTokenAuthenticated(BasePermission):
    """
    Allow any access if keustone token is Authenticated.
    """

    def has_permission(self, request, view):
        return True