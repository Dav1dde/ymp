from urllib.parse import urlparse
import grooveshark
import re

from ymp.types.song import GroovesharkSong
from ymp.types.playlist import Playlist


_GROOVESHARK_PLAYLIST_RE = re.compile(
    r'playlist/(?P<name>[^/]+)/(?P<id>\d+)$'
)


class GroovesharkProvider(object):
    def __init__(self):
        self.grooveshark = grooveshark.Client()
        self.grooveshark.init()

    def responsible_for(self, uri):
        o = urlparse(uri)
        return (
            o.scheme in ('http', 'https') and
            'grooveshark' in o.netloc and
            _GROOVESHARK_PLAYLIST_RE.search(uri)
        )

    def load(self, playlist):
        m = _GROOVESHARK_PLAYLIST_RE.search(playlist)
        if m is None:
            raise ValueError('Invalid grooveshark playlist')

        id = m.group('id')
        p = self.grooveshark.playlist(id)
        # TODO use album cover?
        playlist = Playlist(p.name)

        for song in p.songs:
            playlist.add(GroovesharkSong(song))

        return playlist




