import dbus.service
import dbus

from ymp.dbus.property import PropertyInterface, PropertyList, PropertyType
from ymp.dbus.mediaplayer2 import MediaPlayer2Interface
from ymp.dbus.tracklist import TracklistInterface
from ymp.dbus.playlists import PlaylistsInterface
from ymp.dbus.player import PlayerInterface


class MediaPlayer2(
    PropertyInterface(
        MediaPlayer2Interface.INTERFACE,
        PlayerInterface.INTERFACE,
        TracklistInterface.INTERFACE,
        PlaylistsInterface.INTERFACE
    ),
    MediaPlayer2Interface,
    PlayerInterface,
    TracklistInterface,
    PlaylistsInterface
):
    def __init__(self, backend):
        bus_name = dbus.service.BusName(
            'org.mpris.MediaPlayer2.ymp', bus=dbus.SessionBus()
        )

        dbus.service.Object.__init__(
            self, bus_name, '/org/mpris/MediaPlayer2'
        )

        self.backend = backend

        self._properties = {
            MediaPlayer2Interface.INTERFACE: PropertyList(),
            PlayerInterface.INTERFACE: PropertyList(),
            TracklistInterface.INTERFACE: PropertyList(),
            PlaylistsInterface.INTERFACE: PropertyList()
        }

        MediaPlayer2Interface.register_properties(self._properties, backend)
        PlayerInterface.register_properties(self._properties, backend)
        TracklistInterface.register_properties(self._properties, backend)
        PlaylistsInterface.register_properties(self._properties, backend)

        self.backend.add_notification_callback(self.emit_notification)

    def emit_notification(self, name, value):
        for interface, proplist in self._properties.items():
            if name in proplist:
                return self.PropertiesChanged(interface, {name: value}, [])

        raise ValueError('property "{}" doesn\'t exist'.format(name))

    def get_property(self, interface, property_name):
        return self._properties[interface].get_property(property_name)

    def get_all_properties(self, interface):
        return self._properties[interface].get_all_properties()

    def set_property(self, interface, property_name, value):
        self._properties[interface].set_property(property_name, value)