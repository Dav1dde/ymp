from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject
# from pprint import pprint
import dbus
import time

from ymp.provider.youtube import YoutubeProvider
from ymp.provider import SongProvider
from ymp.backend.vlc import VLCBackend
from ymp.dbus import MediaPlayer2


def main():
    loop = GObject.MainLoop()
    DBusGMainLoop(set_as_default=True)

    pp = SongProvider()
    pp.register_provider(YoutubeProvider())
    pp.add('https://www.youtube.com/playlist?list=PLX9BRxVsfd28lh3cZqqUdAvdLbti41ZQn')
    # print(pp.playlists)
    print('Go!')

    backend = VLCBackend(loop, pp)
    obj = MediaPlayer2(backend)

    loop.run()


if __name__ == '__main__':
    main()
