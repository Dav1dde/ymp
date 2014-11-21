from locale import getpreferredencoding
from subprocess import Popen, PIPE
from urllib.parse import urlparse
import time
import json
import re

from ymp.player.song import Song, TITLE_REGEX, extract_artist_title
from ymp.player.playlist import Playlist
from ymp.provider import Provider
from ymp.lib import pafy


class PafySong(Song):
    def __init__(self, pafy):
        Song.__init__(self, None, pafy.videoid)

        self.pafy = pafy
        self.start = pafy.playlist_meta['start']
        self.end = pafy.playlist_meta['end']

    # we want to load data lazily
    def _update_once(self):
        # if the pafy object has already fetched data once
        # that is enough, since this method does not care
        # about the actual media url, see `update` for more
        if self.pafy._have_basic:
            return

        # we don't need to force it via pafy._have_basic = False
        # but explicitly fetch data if it isn't already
        self.pafy.fetch_basic()

        data = {
            'title': self.pafy.title,
            'user_rating': self.pafy.rating,
            # TODO maybe safe to disc
            'art_url': self.pafy.thumb,
            # pafy.length in seconds, length in microseconds
            'length': self.pafy.length*1000000
        }

        (title, artist) = extract_artist_title(self.pafy.title)
        if title and artist:
            data['title'] = title
            data['artist'] = artist

        self.set_metadata(**data)

    def update(self):
        # TODO maybe make this async, threads?
        # we need to update for expiry at least once
        self._update_once()

        now = time.time()

        # expires in 10 minutes
        if self.pafy.expiry - now < 600:
            # definitly update!
            self.pafy._have_basic = False
            self.pafy.fetch_basic()

    @property
    def uri(self):
        self.update()
        # there is getbestaudio()
        # but for some reason seeking back in a pure audio m4a
        # doesn't seem to work in vlc
        return self.pafy.getbest().url

    @property
    def user_uri(self):
        # no update required
        return self.pafy.watchv_url

    @property
    def metadata(self):
        # we need to set metadata right here
        self._update_once()
        return super().metadata


class _YoutubeProviderBase(Provider):
    def responsible_for(self, uri):
        o = urlparse(uri)
        return (
            o.scheme in ('http', 'https') and
            'youtube' in o.netloc and
            'playlist' in o.path
        )

class YoutubeProviderPafy(_YoutubeProviderBase):
    def __init__(self):
        pass

    def load(self, playlist):
        p = pafy.get_playlist(playlist, basic=False)

        playlist = Playlist(p['title'])

        for item in p['items']:
            playlist.add(PafySong(item['pafy']))

        return playlist


class YoutubeProviderYoutubeDL(_YoutubeProviderBase):
    def __init__(self, youtube_dl='youtube-dl'):
        self.youtube_dl = youtube_dl

    def load(self, playlist):
        p = Popen(
            [self.youtube_dl, '--encoding', 'utf-8', '--dump-json', playlist],
            stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = p.communicate()
        data = list(map(json.loads, stdout.decode('utf-8').splitlines()))

        playlist = Playlist(data[0]['playlist'])

        # getpreferredencoding
        for j in data:
            playlist.add(self.song_from_json(j))

        return playlist

    def song_from_json(self, j):
        if len(j.get('formats', [])) == 0:
            raise ValueError('Invalid JSON, no formats')

        uri = j['formats'][-1]
        aformats = [f for f in j['formats'] if f.get('vcodec') == 'none']
        if len(aformats) > 0:
            uri = aformats[-1]
        uri = uri['url']

        title = j.get('fulltitle', j['title']).strip()

        for r in TITLE_REGEX:
            m = r.match(title)
            if m:
                j.update(m.groupdict({'title': title}))
                break

        for k in ['formats', 'url']:
            j.pop(k)

        j['url'] = j.get('webpage_url', '')
        j['length'] = j.pop('duration')*1000000

        return Song(uri, j.pop('id').replace('-', '_'), **j)


YoutubeProvider = YoutubeProviderPafy
