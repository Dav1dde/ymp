from gi.repository import GObject
import dbus

from dbus.mainloop.glib import DBusGMainLoop

from ymp.dbus import MediaPlayer2
from ymp.backend.vlc import VLCBackend


def main():
    loop = GObject.MainLoop()
    DBusGMainLoop(set_as_default=True)

    backend = VLCBackend(loop)
    obj = MediaPlayer2(backend)

    loop.run()


if __name__ == '__main__':
    main()
