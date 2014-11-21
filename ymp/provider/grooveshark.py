from urllib.parse import urlparse, quote_plus
import grooveshark
import time
import re

from ymp.dbus.types.metadata import Metadata
from ymp.player.playlist import Playlist
from ymp.player.song import Song


_GROOVESHARK_PLAYLIST_RE = re.compile(
    r'playlist/(?P<name>[^/]+)/(?P<id>\d+)$'
)


class GroovesharkSong(Song):
    def __init__(self, song):
        Song.__init__(
            self, None, song.id, title=song.name, artist=song.artist.name,
            album=song.album.name, art_url=song._cover_url
        )

        # maybe duration is None ...
        if song.duration is not None:
            self._metadata[Metadata.LENGTH] = int(song.duration)*1000000

        self.song = song
        self._stream = (0, None)
        # force an update once the stream has been played
        # (or the uri haas been requested from this instance)
        # since grooveshark invalidates stream key
        self._force_update = True

    def update(self):
        if time.time() - self._stream[0] > 600 or self._force_update:
            self._stream = (time.time(), self.song.stream.url)
            self._force_update = False

    @property
    def uri(self):
        self.update()
        self._force_update = True
        return self._stream[1]

    @property
    def user_uri(self):
        return 'http://grooveshark.com/#!/s/{name}/{id}'.format(
            name=quote_plus(self.song.name), id=self.song.id
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
        playlist = Playlist(p.name, icon=p._cover_url)

        for song in p.songs:
            playlist.add(GroovesharkSong(song))

        return playlist

