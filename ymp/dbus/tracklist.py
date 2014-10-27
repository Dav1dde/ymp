import dbus.service

from ymp.dbus.property import PropertyType


class TracklistInterface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2.TrackList'

    @classmethod
    def register_properties(cls, proplist):
        for p in [
            ('Tracks', dbus.Array(signature='o'), PropertyType.read_only),
            ('CanEditTrack', False, PropertyType.read_only),
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.method(
        'org.mpris.MediaPlayer2.TrackList',
        in_signature='ao', out_signature='aa{sv}'
    )
    def GetTracksMetadata(self, trackids):
        return [{}]

    @dbus.service.method(
        'org.mpris.MediaPlayer2.TrackList', in_signature='sob'
    )
    def AddTrack(self, uri, after_track, set_as_current):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.TrackList', in_signature='o')
    def RemoveTrack(self, trackid):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.TrackList', in_signature='o')
    def GoTo(self, trackid):
        pass

    @dbus.service.signal('org.mpris.MediaPlayer2.TrackList', signature='aoo')
    def TrackListReplaced(self, tracks, current_track):
        pass

    @dbus.service.signal('org.mpris.MediaPlayer2.TrackList', signature='a{sv}o')
    def TrackAdded(self, metadata, after_track):
        pass

    @dbus.service.signal('org.mpris.MediaPlayer2.TrackList', signature='o')
    def TrackRemoved(self, trackid):
        pass

    @dbus.service.signal('org.mpris.MediaPlayer2.TrackList', signature='oa{sv}')
    def TrackMetadataChanged(self, trackid, metadata):
        pass
