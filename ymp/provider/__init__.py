from ymp.types.playlist import Playlist, DummyPlaylist
from ymp.types.song import Song


class SongProvider(object):
    def __init__(self):
        self.provider = list()

        self.playlists = dict()
        self._active = DummyPlaylist()

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
        return list(map(Playlist.dbus_playlists, self.playlists.values()))

    def activate_playlist(self, pid):
        self._active = self.playlists[pid]
        self._active.reset()

    @property
    def current_song(self):
        return self._active.current_song

    @property
    def playlist(self):
        return self._active

    @playlist.setter
    def playlist(self, pid):
        self.activate_playlist(pid)

    @property
    def shuffle(self):
        return self._active.shuffle

    @shuffle.setter
    def shuffle(self, value):
        self._active.shuffle = value

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def can_go_next(self):
        return self._active.can_go_next()

    def next(self):
        return self._active.next()

    def can_go_previous(self):
        return self._active.can_go_previous()

    def previous(self):
        return self._active.previous()
