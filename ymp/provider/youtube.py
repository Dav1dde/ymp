from locale import getpreferredencoding
from subprocess import Popen, PIPE
from urllib.parse import urlparse
import json
import re

from ymp.types.playlist import Playlist
from ymp.types.song import Song


class YoutubeProvider(object):
    TITLE_REGEX = [
        re.compile('(?P<artist>[^-]*)\s*-\s*(?P<title>.*)')
    ]

    def __init__(self, youtube_dl='youtube-dl'):
        self.youtube_dl = youtube_dl

    def responsible_for(self, uri):
        o = urlparse(uri)
        return o.scheme in ('http', 'https') and 'youtube' in o.netloc

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

        for r in self.TITLE_REGEX:
            m = r.match(title)
            if m:
                j.update(m.groupdict({'title': title}))
                break

        for k in ['formats', 'url']:
            j.pop(k)

        j['url'] = j.get('webpage_url', '')
        j['length'] = j.pop('duration')*1000000

        return Song(uri, j.pop('id').replace('-', '_'), **j)
