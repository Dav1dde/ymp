import dbus.service
import dbus

from ymp.dbus.types.metadata import Metadata


class Song(object):
    DEFINED_METADATA = dict(
        (e, getattr(Metadata, e)) for e in dir(Metadata)
    )

    def __init__(self, uri, id, **kwargs):
        self.uri = uri
        self.id = id
        if not self.id.startswith('/'):
            self.id = '/{}'.format(self.id)

        self._metadata = dict()
        for k, v in kwargs.items():
            if v is None:
                continue

            key = 'ymp:{}'.format(k)
            if k.upper() in self.DEFINED_METADATA:
                key = self.DEFINED_METADATA[k.upper()]

            self._metadata[key] = v

    @property
    def metadata(self):
        m = Metadata(self._metadata)
        m[Metadata.URL] = self.uri
        m[Metadata.TRACKID] = dbus.service.ObjectPath(self.id)
        if Metadata.LENGTH in m:
            m[Metadata.LENGTH] = dbus.Int64(m[Metadata.LENGTH])
        if Metadata.ARTIST in m:
            m[Metadata.ARTIST] = [m[Metadata.ARTIST]]
        return m

    def __repr__(self):
        return 'Song({0!r})'.format(dict(self.metadata))
