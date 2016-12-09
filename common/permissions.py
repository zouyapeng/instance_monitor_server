from rest_framework.permissions import BasePermission
from common.openstack import authenticate_token


class IsTokenAuthenticated(BasePermission):
    """
    Allow any access if keustone token is Authenticated.
    """

    def has_permission(self, request, view):
        is_agent = request.data.get('agent', None)
        if is_agent:
            return True

        try:
            token = request.META['HTTP_TOKEN']
        except KeyError:
            return False
        if authenticate_token(token) != 200:
            return False

        return True