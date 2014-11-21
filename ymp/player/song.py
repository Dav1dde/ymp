
import dbus.service
import dbus
import time
import re

from ymp.dbus.types.metadata import Metadata
from ymp.utility import dbus_path


TITLE_REGEX = [
    re.compile('(?P<artist>[^-]*)\s*-\s*(?P<title>.*)')
]


def extract_artist_title(s):
    for r in TITLE_REGEX:
        m = r.match(s)
        if m:
            return (m.group('title'), m.group('artist'))

    return (s, '')


class Song(object):
    DEFINED_METADATA = dict(
        (e, getattr(Metadata, e)) for e in dir(Metadata)
    )

    def __init__(self, uri, id, **kwargs):
        self._uri = uri
        self._id = dbus_path(id)

        self.start = None  # start audio from position (seconds)
        self.end = None  # stop audio at position (seconds)

        self._metadata = dict()
        if kwargs:
            self.set_metadata(**kwargs)

    def set_metadata(self, **kwargs):
        self._metadata = dict()
        for k, v in kwargs.items():
            if v is None:
                continue

            key = 'ymp:{}'.format(k)
            if k.upper() in self.DEFINED_METADATA:
                key = self.DEFINED_METADATA[k.upper()]

            self._metadata[key] = v

    # might be called soon before this song is played
    # the song might not be played, or this method
    # isn't called at all, even if the song will be played.
    def update(self):
        pass

    @property
    def uri(self):
        return self._uri

    @property
    def user_uri(self):
        return self.uri

    @property
    def id(self):
        return self._id

    @property
    def metadata(self):
        m = Metadata(self._metadata)
        uu = self.user_uri
        if uu:
            m[Metadata.URL] = uu
        m[Metadata.TRACKID] = dbus.service.ObjectPath(self.id)
        if Metadata.LENGTH in m:
            m[Metadata.LENGTH] = dbus.Int64(m[Metadata.LENGTH])
        if Metadata.ARTIST in m:
            m[Metadata.ARTIST] = [m[Metadata.ARTIST]]
        return m

    def __repr__(self):
        return 'Song({0!r})'.format(dict(self.metadata))


