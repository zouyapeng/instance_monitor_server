from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneauth1.exceptions.http import Unauthorized, NotFound
from keystoneauth1.exceptions import ConnectFailure, ConnectTimeout
from django.conf import settings


def authenticate_token(token):
    auth = v2.Token(auth_url=settings.OPENSTACK_AUTH_URL, token=token)
    sess = session.Session(auth=auth, timeout=2)
    try:
        sess.get_auth_headers()
        return 200
    except Unauthorized:
        return 401
    except ConnectFailure:
        return 404
    except ConnectTimeout:
        return 504