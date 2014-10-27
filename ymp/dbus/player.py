import dbus.service
import dbus

from ymp.dbus.types.metadata import Metadata
from ymp.dbus.property import PropertyType


class PlayerInterface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2.Player'

    @classmethod
    def register_properties(cls, proplist, backend):
        for p in [
            ('PlaybackStatus', backend.playback_status, PropertyType.read_only),
            ('LoopStatus', backend.loop_status, PropertyType.read_write),
            ('Rate', backend.rate, PropertyType.read_write),
            ('Shuffle', backend.shuffle, PropertyType.read_write),
            ('Metadata', backend.metadata, PropertyType.read_only),
            ('Volume', backend.volume, PropertyType.read_write),
            ('Position', backend.position, PropertyType.read_only),
            ('MinimumRate', backend.minimum_rate, PropertyType.read_only),
            ('MaximumRate', backend.maximum_rate, PropertyType.read_only),
            ('CanGoNext', backend.can_go_next, PropertyType.read_only),
            ('CanGoPrevious', backend.can_go_previous, PropertyType.read_only),
            ('CanPlay', backend.can_play, PropertyType.read_only),
            ('CanPause', backend.can_pause, PropertyType.read_only),
            ('CanSeek', backend.can_seek, PropertyType.read_only),
            ('CanControl', backend.can_control, PropertyType.read_only),
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.signal('org.mpris.MediaPlayer2.Player', signature='x')
    def Seeked(self, position):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Next(self):
        self.backend.next()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Previous(self):
        self.backend.previous()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Pause(self):
        self.backend.pause()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def PlayPause(self):
        # TODO check CanPlay
        self.backend.play_pause()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Stop(self):
        self.backend.stop()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Play(self):
        # TODO check CanPlay
        self.backend.play()

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='x')
    def Seek(self, offset):
        # TODO check CanSeek
        self.backend.seek(offset)

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='ox')
    def SetPosition(self, trackid, position):
        # TODO check if trackid matches current trackid
        if position < 0:
            return
        self.backend.set_position(trackid, position)

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='s')
    def OpenUri(self, uri):
        self.backend.open_uri(uri)
