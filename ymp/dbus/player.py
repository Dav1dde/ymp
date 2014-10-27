import dbus.service
import dbus

from ymp.dbus.types.metadata import Metadata
from ymp.dbus.property import PropertyType


class PlayerInterface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2.Player'

    @classmethod
    def register_properties(cls, proplist):
        for p in [
            ('PlaybackStatus', 'Paused', PropertyType.read_only),
            # ('LoopStatus', 'Track', PropertyType.read_write),
            ('Rate', 1.0, PropertyType.read_write),
            ('Shuffle', False, PropertyType.read_write),
            ('Metadata', Metadata(), PropertyType.read_only),
            ('Volume', 1.0, PropertyType.read_write),
            ('Position', dbus.Int64(0), PropertyType.read_only),
            ('MinimumRate', 1.0, PropertyType.read_only),
            ('MaximumRate', 1.0, PropertyType.read_only),
            ('CanGoNext', True, PropertyType.read_only),
            ('CanGoPrevious', True, PropertyType.read_only),
            ('CanPlay', True, PropertyType.read_only),
            ('CanPause', True, PropertyType.read_only),
            ('CanSeek', False, PropertyType.read_only),
            ('CanControl', True, PropertyType.read_only),
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.signal('org.mpris.MediaPlayer2.Player', signature='x')
    def Seeked(self, position):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Next(self):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Previous(self):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Pause(self):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def PlayPause(self):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Stop(self):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Play(self):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='x')
    def Seek(self, offset):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='ox')
    def SetPosition(self, trackid, position):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='s')
    def OpenUri(self, uri):
        pass
