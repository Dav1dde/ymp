import dbus.service
import dbus

from ymp.dbus.property import PropertyType


class PlaylistsInterface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2.Playlists'

    @classmethod
    def register_properties(cls, proplist):
        for p in [
            ('PlaylistCount', 0, PropertyType.read_only),
            ('Orderings', dbus.Array(signature='as'), PropertyType.read_only),
            ('ActivePlaylist', dbus.Struct((False, ('/test', '', '')), signature='(oss)'), PropertyType.read_only)
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.method('org.mpris.MediaPlayer2.Playlists', in_signature='o')
    def ActivatePlaylist(self, trackids):
        pass

    @dbus.service.method(
        'org.mpris.MediaPlayer2.Playlists',
        in_signature='uusb', out_signature='a(oss)'
    )
    def GetPlaylists(self, index, max_count, order, reveresed):
        return [('/I/am/awesome', 'Boss Playlist', '')]

    @dbus.service.method('org.mpris.MediaPlayer2.Playlists', signature='(oss)')
    def PlaylistChanged(self, paylist):
        pass
