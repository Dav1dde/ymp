from urllib.parse import urlparse
import soundcloud
import re

from ymp.types.song import SoundCloudSong
from ymp.types.playlist import Playlist


_SOUND_CLOUD_SET_RE = re.compile(
    r'/(?P<author>[\w,\-,_]+)/sets/(?P<playlist>[\w,\-,_]+)$'
)


class SoundCloudProvider(object):
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




