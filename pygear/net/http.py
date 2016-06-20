import base64
from six.moves.urllib.request import getproxies, proxy_bypass
from six.moves.urllib.parse import unquote, urlunparse

try:
    from urllib2 import _parse_proxy
except ImportError:
    from urllib.request import _parse_proxy


def get_proxy(url, orig_type):
    proxy_type, user, password, hostport = _parse_proxy(url)
    proxy_url = urlunparse((proxy_type or orig_type, hostport, '', '', '', ''))

    if user and password:
        user_pass = '%s:%s' % (unquote(user), unquote(password))
        creds = base64.b64encode(user_pass).strip()
    else:
        creds = None

    return creds, proxy_url