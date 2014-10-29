

class Playlist(tuple):
    def __new__(cls, *args):
        return super(Playlist, cls).__new__(cls, args)

    @property
    def id(self):
        return self[0]

    @property
    def name(self):
        return self[1]

    @property
    def icon(self):
        return self[2]


class MaybePlaylist(tuple):
    def __new__(cls, valid, pid, name, icon):
        return super(MaybePlaylist, cls).__new__(
            cls, (valid, Playlist(pid, name, icon))
        )

    @property
    def valid(self):
        return self[0]

    @property
    def playlist(self):
        return self[1]
