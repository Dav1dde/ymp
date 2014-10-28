


class Provider(object):
    def __init__(self):
        self.provider = list()

        self.playlists = list()

    def register_provider(self, provider):
        self.provider.append(provider)

    def add(self, playlist):
        for p in self.provider:
            if p.responsible_for(playlist):
                self.playlists.append(p.load(playlist))

    def load_from_file(self, path):
        with open(path) as f:
            for line in f:
                self.add(line.strip())

