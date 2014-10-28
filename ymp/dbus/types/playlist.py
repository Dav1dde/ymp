

class Playlist(tuple):
    def __init__(self, pid, name, icon):
        tuple.__init__(self, (pid, name, icon))

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
    def __init__(self, valid, pid, name, icon):
        tuple.__init__(self, (valid, Playlist(pid, name, icon)))

    @property
    def valid(self):
        return self[0]

    @property
    def playlist(self):
        return self[1]
