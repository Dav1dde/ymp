from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject
# from pprint import pprint
import argparse
import dbus
import time

from ymp.provider.grooveshark import GroovesharkProvider
from ymp.provider.soundcloud import SoundCloudProvider
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
    parser = argparse.ArgumentParser('ymp', fromfile_prefix_chars='@')

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
        '--soundcloud', dest='soundcloud', default=None,
        help='Soundcloud client id, can be generated for free'
    )

    parser.add_argument(
        '-r', '--repeat', dest='repeat', action='store_true',
        help='Play playlists on repeat'
    )

    parser.add_argument(
        '--backend', dest='backend', type=_backend, default=VLCBackend,
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

    pp.register_provider(YoutubeProvider())
    if ns.soundcloud:
        pp.register_provider(SoundCloudProvider(ns.soundcloud))
    pp.register_provider(GroovesharkProvider())

    playlists = set(filter(bool, map(str.strip, ns.playlist or [])))
    for line in ns.pf or []:
        playlists.add(line.strip())

    for playlist in playlists:
        pp.add(playlist)

    backend = ns.backend(loop, pp, ns.backend_options)
    obj = MediaPlayer2(backend)

    loop.run()


if __name__ == '__main__':
    main()
