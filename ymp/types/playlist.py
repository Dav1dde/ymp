import random

from ymp.dbus.types.playlist import Playlist as DBusPlaylist
from ymp.exception import YmpPlaylistException
from ymp.utility import dbus_path


class Playlist(object):
    PLAYLISTS = 0

    def __init__(self, name, icon='', id=None, endless=False):
        self.name = name
        self.icon = icon
        self.id = id
        if self.id is None:
            self.id = '{}_{}'.format(name, self.PLAYLISTS+1)
            self.PLAYLISTS += 1

        self.id = dbus_path(self.id)

        self.endless = endless

        self.songs = list()
        self._songs = list()
        self._shuffle = False

        self._current = 0

    @property
    def dbus_playlist(self):
        return DBusPlaylist(self.id, self.name, self.icon)

    @property
    def shuffle(self):
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value):
        if not value == self._shuffle:
            self.reset()
            if value:
                random.shuffle(self._songs)

        self._shuffle = value

    def add(self, song, index=None):
        index = len(self.songs) if index is None else index
        self.songs.insert(index, song)
    insert = add

    def __repr__(self):
        return '{0}({1}, {2!r})'.format(
            self.__class__.__name__, self.name, self.songs
        )

    def reset(self):
        self._current = 0
        self._songs = list(self.songs)

    @property
    def current_song(self):
        return self._songs[self._current]

    @property
    def has_next(self):
        return self.endless or (self._current+1) < len(self._songs)

    def play_next(self):
        if not self.has_next:
            raise YmpPlaylistException('playlist reached the end')

        self._current = (self._current + 1) % len(self._songs)
        return self._songs[self._current]

    @property
    def next(self):
        if not self.has_next:
            raise YmpPlaylistException('playlist has no next song')

        next = (self._current + 1) % len(self._songs)
        return self._songs[next]

    @property
    def has_previous(self):
        return self.endless or self._current > 0

    def play_previous(self):
        if not self.has_previous:
            raise YmpPlaylistException('can\'t go to previous song')

        self._current = (self._current - 1) % len(self._songs)
        return self.songs[self._current]

    @property
    def previous(self):
        if not self.has_previous:
            raise YmpPlaylistException('playlist has no previous song')

        previous = (self._current - 1) % len(self._songs)
        return self._songs[previous]
