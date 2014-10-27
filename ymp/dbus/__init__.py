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
    def __init__(self):
        bus_name = dbus.service.BusName(
            'org.mpris.MediaPlayer2.ymp', bus=dbus.SessionBus()
        )

        dbus.service.Object.__init__(
            self, bus_name, '/org/mpris/MediaPlayer2'
        )

        self._properties = {
            MediaPlayer2Interface.INTERFACE: PropertyList(),
            PlayerInterface.INTERFACE: PropertyList(),
            TracklistInterface.INTERFACE: PropertyList(),
            PlaylistsInterface.INTERFACE: PropertyList()
        }

        MediaPlayer2Interface.register_properties(self._properties)
        PlayerInterface.register_properties(self._properties)
        TracklistInterface.register_properties(self._properties)
        PlaylistsInterface.register_properties(self._properties)

    def get_all_properties(self, interface):
        return self._properties[interface].get_all_properties()

    def properties_changed(self, interface, changed_properties, invalidated_properties):
        self._properties[interface].properties_changed(
            changed_properties, invalidated_properties
        )
