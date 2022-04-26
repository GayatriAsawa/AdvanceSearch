"""file for ifm LDAP server setup and usage."""

from ldap3 import *
from django.conf import settings


def check_credentials(username, password):
    """function for checking server response to check credentials request."""
    try: 
        server = Server(settings.IFM_LDAP_SERVER, )
        conn = Connection(server, user=username, password=password)
        if conn:
            message = "loggedin"
            return message
        else:
            message = 'invalid_login'
            return message
    except:
        message = "User login failed !"
        return message
