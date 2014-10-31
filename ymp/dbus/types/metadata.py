import dbus


class Metadata(dbus.Dictionary):
    ART_URL = 'mpris:artUrl'
    TRACKID = 'mpris:trackid'
    LENGTH = 'mpris:length'
    ALBUM = 'xesam:album'
    ALBUM_ARTIST = 'xesam:albumArtist'
    ARTIST = 'xesam:artist'
    AS_TEXT = 'xesam:asText'
    AUDIO_BPM = 'xesam:audioBPM'
    AUTO_RATING = 'xesam:autoRating'
    COMMENT = 'xesam:comment'
    COMPOSER = 'xesam:composer'
    CONTENT_CREATED = 'xesam:contentCreated'
    DISC_NUMBER = 'xesam:discNumber'
    FIRST_USED = 'xesam:firstUsed'
    GENRE = 'xesam:genre'
    LAST_USED = 'xesam:lastUsed'
    LYRICIST = 'xesam:lyricist'
    TITLE = 'xesam:title'
    TRACK_NUMBER = 'xesam:trackNumber'
    URL = 'xesam:url'
    USE_COUNT = 'xesam:useCount'
    USER_RATING = 'xesam:userRating'

    def __init__(self, data=()):
        dbus.Dictionary.__init__(self, data, signature='sv', variant_level=1)
