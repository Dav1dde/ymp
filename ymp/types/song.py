from urllib.parse import quote_plus
import dbus.service
import dbus
import time
import re

from ymp.dbus.types.metadata import Metadata
from ymp.utility import dbus_path


TITLE_REGEX = [
    re.compile('(?P<artist>[^-]*)\s*-\s*(?P<title>.*)')
]


def extract_artist_title(s):
    for r in TITLE_REGEX:
        m = r.match(s)
        if m:
            return (m.group('title'), m.group('artist'))

    return (s, '')


class Song(object):
    DEFINED_METADATA = dict(
        (e, getattr(Metadata, e)) for e in dir(Metadata)
    )

    def __init__(self, uri, id, **kwargs):
        self._uri = uri
        self._id = dbus_path(id)

        self.start = None  # start audio from position (seconds)
        self.end = None  # stop audio at position (seconds)

        self._metadata = dict()
        if kwargs:
            self.set_metadata(**kwargs)

    def set_metadata(self, **kwargs):
        self._metadata = dict()
        for k, v in kwargs.items():
            if v is None:
                continue

            key = 'ymp:{}'.format(k)
            if k.upper() in self.DEFINED_METADATA:
                key = self.DEFINED_METADATA[k.upper()]

            self._metadata[key] = v

    # might be called soon before this song is played
    # the song might not be played, or this method
    # isn't called at all, even if the song will be played.
    def update(self):
        pass

    @property
    def uri(self):
        return self._uri

    @property
    def user_uri(self):
        return self.uri

    @property
    def id(self):
        return self._id

    @property
    def metadata(self):
        m = Metadata(self._metadata)
        uu = self.user_uri
        if uu:
            m[Metadata.URL] = uu
        m[Metadata.TRACKID] = dbus.service.ObjectPath(self.id)
        if Metadata.LENGTH in m:
            m[Metadata.LENGTH] = dbus.Int64(m[Metadata.LENGTH])
        if Metadata.ARTIST in m:
            m[Metadata.ARTIST] = [m[Metadata.ARTIST]]
        return m

    def __repr__(self):
        return 'Song({0!r})'.format(dict(self.metadata))


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
