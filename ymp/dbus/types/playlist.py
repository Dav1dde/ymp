

class Playlist(tuple):
    def __init__(self, pid, name, icon):
        tuple.__init__(self, (pid, name, icon))


class MaybePlaylist(tuple):
    def __init__(self, valid, pid, name, icon):
        tuple.__init__(self, (valid, (pid, name, icon)))