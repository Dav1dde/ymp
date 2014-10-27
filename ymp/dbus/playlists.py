import dbus.service
import dbus

from ymp.dbus.property import PropertyType


class PlaylistsInterface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2.Playlists'

    @classmethod
    def register_properties(cls, proplist, backend):
        for p in [
            ('PlaylistCount', backend.playlist_count, PropertyType.read_only),
            ('Orderings', backend.orderings, PropertyType.read_only),
            ('ActivePlaylist', backend.active_playlist, PropertyType.read_only)
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.method('org.mpris.MediaPlayer2.Playlists', in_signature='o')
    def ActivatePlaylist(self, trackids):
        self.backend.activate_playlist(trackids)

    @dbus.service.method(
        'org.mpris.MediaPlayer2.Playlists',
        in_signature='uusb', out_signature='a(oss)'
    )
    def GetPlaylists(self, index, max_count, order, reversed_):
        return self.backend.get_playlists(index, max_count, order, reversed_)

    @dbus.service.signal('org.mpris.MediaPlayer2.Playlists', signature='(oss)')
    def PlaylistChanged(self, paylist):
        pass
