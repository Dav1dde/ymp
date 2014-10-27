import dbus.service

from ymp.dbus.property import PropertyType


class MediaPlayer2Interface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2'

    @classmethod
    def register_properties(cls, proplist):
        for p in [
            ('CanQuit', False, PropertyType.read_only),
            # ('Fullscreen', False, PropertyType.read_write),
            # ('CanSetFullscreen', False, PropertyType.read_only),
            ('CanRaise', False, PropertyType.read_only),
            ('HasTrackList', True, PropertyType.read_only),
            ('Identity', 'Youtube media player', PropertyType.read_only),
            ('DesktopEntry', 'ymp', PropertyType.read_only),
            ('SupportedUriSchemes', ['http'], PropertyType.read_only),
            ('SupportedMimeTypes', ['text/html'], PropertyType.read_only)
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.method('org.mpris.MediaPlayer2')
    def Raise(self):
        pass

    @dbus.service.method('org.mpris.MediaPlayer2')
    def Quit(self):
        print('quit')
