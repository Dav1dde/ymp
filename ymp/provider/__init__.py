import operator

from ymp.types.playlist import Playlist, DummyPlaylist
from ymp.types.song import Song


class SongProvider(object):
    def __init__(self):
        self.provider = list()

        self.playlists = dict()
        self._active = None
        self._shuffle = False

    def register_provider(self, provider):
        self.provider.append(provider)

    def add(self, playlist):
        for provider in self.provider:
            if provider.responsible_for(playlist):
                p = provider.load(playlist)
                self.playlists[p.id] = p

    def load_from_file(self, path):
        with open(path) as f:
            for line in f:
                self.add(line.strip())

    @property
    def dbus_playlists(self):
        return list(map(
            operator.attrgetter('dbus_playlist'), self.playlists.values()
        ))

    def activate_playlist(self, pid):
        self._active = self.playlists[pid]
        self._active.reset()
        self._active.shuffle = self._shuffle

    @property
    def current_playlist(self):
        return self._active

    @current_playlist.setter
    def current_playlist(self, pid):
        self.activate_playlist(pid)

    @property
    def current_song(self):
        return self._active.current_song if self._active else None

    @property
    def shuffle(self):
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value):
        self._shuffle = value
        if self._active is not None:
            self._active.shuffle = value

    def can_go_next(self):
        return self._active is not None and self._active.can_go_next()

    def next(self):
        return self._active.next()

    def can_go_previous(self):
        return self._active is not None and self._active.can_go_previous()

    def previous(self):
        return self._active.previous()
