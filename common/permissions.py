from rest_framework.permissions import BasePermission
from common.openstack import authenticate_token


class IsTokenAuthenticated(BasePermission):
    """
    Allow any access if keustone token is Authenticated.
    """

    def has_permission(self, request, view):
        try:
            token = request.META['HTTP_X_AUTH_TOKEN']
        except KeyError:
            return False
        if authenticate_token(token) != 200:
            return False

        return True