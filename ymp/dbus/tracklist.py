import dbus.service

from ymp.dbus.property import PropertyType


class TracklistInterface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2.TrackList'

    @classmethod
    def register_properties(cls, proplist, backend):
        for p in [
            ('Tracks', backend.tracks, PropertyType.read_only),
            ('CanEditTrack', backend.can_edit_track, PropertyType.read_only),
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.method(
        'org.mpris.MediaPlayer2.TrackList',
        in_signature='ao', out_signature='aa{sv}'
    )
    def GetTracksMetadata(self, trackids):
        return self.backend.get_tracks_metadata(trackids)

    @dbus.service.method(
        'org.mpris.MediaPlayer2.TrackList', in_signature='sob'
    )
    def AddTrack(self, uri, after_track, set_as_current):
        self.backend.add_track(uri, after_track, set_as_current)

    @dbus.service.method('org.mpris.MediaPlayer2.TrackList', in_signature='o')
    def RemoveTrack(self, trackid):
        self.backend.remove_track(trackid)

    @dbus.service.method('org.mpris.MediaPlayer2.TrackList', in_signature='o')
    def GoTo(self, trackid):
        self.backend.goto(trackid)

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
