from gi.repository import GObject
import dbus

from dbus.mainloop.glib import DBusGMainLoop

from ymp.dbus import MediaPlayer2


def main():
    loop = GObject.MainLoop()
    DBusGMainLoop(set_as_default=True)

    obj = MediaPlayer2()

    loop.run()


if __name__ == '__main__':
    main()