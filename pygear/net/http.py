import base64

from pygear.core.six.moves.urllib.parse import unquote, urlunparse
from pygear.text.encoding import force_bytes

try:
    from urllib2 import _parse_proxy
except ImportError:
    from urllib.request import _parse_proxy


def get_proxy(url, orig_type):
    proxy_type, user, password, hostport = _parse_proxy(url)
    proxy_url = urlunparse((proxy_type or orig_type, hostport, '', '', '', ''))

    if user and password:
        user_pass = '%s:%s' % (unquote(user), unquote(password))
        creds = base64.b64encode(force_bytes(user_pass)).strip()
    else:
        creds = None

    return creds, proxy_url