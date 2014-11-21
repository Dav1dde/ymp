from urllib.parse import urlparse
import soundcloud
import re

from ymp.player.song import Song, extract_artist_title
from ymp.player.playlist import Playlist
from ymp.provider import Provider


_SOUND_CLOUD_SET_RE = re.compile(
    r'/(?P<author>[\w,\-,_]+)/sets/(?P<playlist>[\w,\-,_]+)$'
)


class SoundCloudSong(Song):
    def __init__(self, track, soundcloud):
        if 'stream_url' not in track:
            raise ValueError('Unable to retrieve stream url from soundcloud')

        (title, artist) = extract_artist_title(track['title'])

        Song.__init__(
            self, None, str(track['id']), title=title, artist=artist,
            art_url=track['artwork_url'], length=track['duration']*1000
        )

        self.track = track
        self.soundcloud = soundcloud

    def update(self):
        if self._uri is not None:
            return

        self._uri = self.soundcloud.get(
            self.track['stream_url'], allow_redirects=False
        ).location

    @property
    def uri(self):
        self.update()
        return self._uri

    @property
    def user_uri(self):
        return self.track['permalink_url']


class SoundCloudProvider(Provider):
    def __init__(self, client_id):
        self.soundcloud = soundcloud.Client(client_id=client_id)

    def responsible_for(self, uri):
        o = urlparse(uri)
        return (
            o.scheme in ('http', 'https') and
            'soundcloud' in o.netloc and
            _SOUND_CLOUD_SET_RE.search(o.path)
        )

    def load(self, playlist):
        m = _SOUND_CLOUD_SET_RE.search(playlist)
        if m is None:
            raise ValueError('Invalid Soundcloud playlist')

        # TODO extract numeric id from playlist url
        # playlistname is maybe not unique?
        pl = m.group('playlist')
        r = self.soundcloud.get('playlists/{}'.format(pl))

        playlist = Playlist(pl, icon=getattr(r, 'artwork_url', ''))

        for track in r.tracks:
            if 'stream_url' not in track:
                continue

            playlist.add(SoundCloudSong(track, self.soundcloud))

        return playlist

