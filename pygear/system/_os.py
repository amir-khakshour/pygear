import sys
from pygear.core import six

if six.PY2:
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()


def upath(path):
    """
    Always return a unicode path.
    """
    if six.PY2 and not isinstance(path, six.text_type):
        return path.decode(fs_encoding)
    return path