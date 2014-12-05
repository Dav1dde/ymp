from dbus.mainloop.glib import DBusGMainLoop
from itertools import zip_longest
from gi.repository import GObject
# from pprint import pprint
import configparser
import argparse
import inspect
import dbus
import time
import sys
import os

from ymp.provider.grooveshark import GroovesharkProvider
from ymp.provider.soundcloud import SoundCloudProvider
from ymp.provider.youtube import YoutubeProvider
from ymp.player.ymp import YmpMediaPlayer
from ymp.backend.vlc import VLCBackend
from ymp.dbus import MediaPlayer2


CONFIG_PATH = os.path.expanduser('~/.config/ymp/')
CONFIG_FILE = os.path.join(CONFIG_PATH, 'ymp.conf')

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)


class ValidationError(Exception):
    def __init__(self, key, value, validator):
        self.key = key
        self.value = value
        self.validator = validator
        self.message = inspect.getdoc(validator)

    def __str__(self):
        return (
            'Unable to validate entry `{self.key}: {self.value}`: '
            '{self.message}'.format(self=self)
        )


def config_bool(b):
    '''boolean expected'''
    if isinstance(b, str):
        if not b.lower() in ('yes', '1', 'true', 'on',
                             'no', '0', 'false', 'off'):
            raise ValueError
        return b.lower() in ('yes', '1', 'true', 'on')
    raise ValueError


def config_file(path, mode='r'):
    '''unable to open file'''
    path = os.path.expanduser(path)
    try:
        f = open(path, mode)
    except IOError:
        raise ValueError()

    return f


def config_backend(name):
    '''invalid backend'''
    try:
        backend = _backend(name)
    except argparse.ArgumentTypeError:
        raise ValueError
    return backend


# (func, [])
def validate_config(items, *args):
    validators = dict()
    for validator, keys in args:
        validators.update(zip_longest(keys, [], fillvalue=validator))

    null_validator = lambda x: x

    result = list()
    for key, value in items:
        validator = validators.get(key, null_validator)
        try:
            value = validator(value)
        except ValueError:
            raise ValidationError(key, value, validator)
        result.append((key, value))

    return result


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
        '--config', dest='config', metavar='FILE', default=None,
        type=argparse.FileType('r'), help='Path to a configfile'
    )

    defaults = dict()
    if '-h' not in sys.argv and '--help' not in sys.argv:
        arg, remaining_args = parser.parse_known_args()

        config = configparser.ConfigParser()
        config.read(arg.config or CONFIG_FILE)
        try:
            items = validate_config(
                config.items('ymp'),
                (config_file, ['playlist_file']),
                (config_bool, ['shuffle', 'repeat']),
                (config_backend, ['backend']),
            )
        except ValidationError as e:
            return parser.error(str(e))
        defaults.update(items)
    else:
        remaining_args = sys.argv

    parser.add_argument(
        '-f', '--playlist-file', dest='playlist_file',
        type=argparse.FileType('r'), metavar='FILE',
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

    parser.set_defaults(**defaults)
    ns = parser.parse_args(remaining_args)

    loop = GObject.MainLoop()
    DBusGMainLoop(set_as_default=True)

    pp = YmpMediaPlayer()
    pp.shuffle = ns.shuffle
    pp.repeat = ns.repeat

    pp.register_provider(YoutubeProvider())
    if ns.soundcloud:
        pp.register_provider(SoundCloudProvider(ns.soundcloud))
    pp.register_provider(GroovesharkProvider())

    playlists = set(filter(bool, map(str.strip, ns.playlist or [])))
    for line in ns.playlist_file or []:
        playlists.add(line.strip())
    ns.playlist_file.close()

    for playlist in playlists:
        pp.add(playlist)

    backend = ns.backend(loop, pp, ns.backend_options)
    obj = MediaPlayer2(backend)

    loop.run()


if __name__ == '__main__':
    main()
