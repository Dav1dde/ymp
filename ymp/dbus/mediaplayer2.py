import dbus.service

from ymp.dbus.property import PropertyType


class MediaPlayer2Interface(dbus.service.Object):
    INTERFACE = 'org.mpris.MediaPlayer2'

    @classmethod
    def register_properties(cls, proplist, backend):
        for p in [
            ('CanQuit', backend.can_quit, PropertyType.read_only),
            ('Fullscreen', backend.fullscreen, PropertyType.read_write),
            ('CanSetFullscreen', backend.can_set_fullscreen, PropertyType.read_only),
            ('CanRaise', backend.can_raise, PropertyType.read_only),
            ('HasTrackList', backend.has_track_list, PropertyType.read_only),
            ('Identity', 'Youtube media player', PropertyType.read_only),
            ('DesktopEntry', 'ymp', PropertyType.read_only),
            ('SupportedUriSchemes', ['http'], PropertyType.read_only),
            ('SupportedMimeTypes', ['text/html'], PropertyType.read_only)
        ]:
            proplist[cls.INTERFACE].add_property(*p)

    @dbus.service.method('org.mpris.MediaPlayer2')
    def Raise(self):
        self.backend.raise_()

    @dbus.service.method('org.mpris.MediaPlayer2')
    def Quit(self):
        self.backend.quit()
