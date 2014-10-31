import re


_DBUS_PATH_RE = re.compile(r'[^\w,^\d,^_]')


def dbus_path(*args):
    s = '/'.join(a.strip('/') for a in args if a.strip('/'))
    s = _DBUS_PATH_RE.sub('_', s)
    return '/{}'.format(s)
