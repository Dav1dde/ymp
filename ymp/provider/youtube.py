from subprocess import Popen, PIPE
from urllib.parse import urlparse
import json


class YoutubeProvider(object):
    def __init__(self, youtube_dl='youtube-dl'):
        self.youtube_dl = youtube_dl

    def responsible_for(self, uri):
        o = urlparse(uri)
        return o.scheme == 'http' and 'youtube' in o.netloc

    def load(self, playlist):
        p = Popen(
            [self.youtube_dl, '--dump-json', playlist],
            stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = p.communicate()

        for line in stdout.splitlines():
            return self.from_json(json.loads(line))

    def from_json(self, j):
        if len(j.get('formats', [])) == 0:
            raise ValueError('Invalid JSON, no formats')

        format = j['formats'][-1]
        aformats = [f for f in j['formats'] if f.get('vcodec') == 'none']
        if len(aformats) > 0:
            format = aformats[-1]

        return (j['playlist'])