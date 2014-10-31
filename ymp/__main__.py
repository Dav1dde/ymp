'''
Yolo Media Player or Youtube Media Player

This media player currently supports Youtube playlists and
exports a Mpris2 interface to control it.

Recommended gnome plugin: https://extensions.gnome.org/extension/55/media-player-indicator/

Future features:
  * Grooveshark
  * Webinterface
  * m3u/pls playlists
  * multiple backends (probably)
  * multiple mainloops (maybe)
'''

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject
# from pprint import pprint
import argparse
import dbus
import time

from ymp.provider.youtube import YoutubeProvider
from ymp.provider import SongProvider
from ymp.backend.vlc import VLCBackend
from ymp.dbus import MediaPlayer2


def _backend(name):
    try:
        return {
            'vlc': VLCBackend
        }[name.lower()]
    except KeyError:
        raise argparse.ArgumentTypeError('Invalid backend "{}"'.format(name))


def main():
    parser = argparse.ArgumentParser(__doc__, fromfile_prefix_chars='@')

    parser.add_argument(
        '-f', '--playlist-file', dest='pf', type=argparse.FileType('r'),
        help='Path to a newline separated file of playlists'
    )

    parser.add_argument(
        '-p', '--playlist', nargs='*', dest='playlist',
        help='List of playlists'
    )

    parser.add_argument(
        '-s', '--shuffle', dest='shuffle', action='store_true',
        help='Shuffle songs of a playlist'
    )

    parser.add_argument(
        '-r', '--repeat', dest='repeat', action='store_true',
        help='Play playlists on repeat'
    )

    parser.add_argument(
        '--backend', dest='backend', type=_backend,
        help='Sound backend for playing music. Currently only supports VLC'
    )

    parser.add_argument(
        '--backend-options', dest='backend_options', default='',
        help='String containing additional options '
        'for the backend, this is backend specfic!'
    )

    ns = parser.parse_args()

    loop = GObject.MainLoop()
    DBusGMainLoop(set_as_default=True)

    pp = SongProvider()
    pp.shuffle = ns.shuffle
    pp.repeat = ns.repeat

    playlists = set(map(str.strip, ns.playlist))
    for line in ns.pf or []:
        playlists.add(line.strip())

    for playlist in playlists:
        pp.add(playlist)

    backend = ns.backend(loop, pp, ns.backend_options)
    obj = MediaPlayer2(backend)

    loop.run()


if __name__ == '__main__':
    main()
