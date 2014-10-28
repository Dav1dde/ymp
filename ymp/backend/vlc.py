from ymp.dbus.types.playlist import Playlist, MaybePlaylist
from ymp.dbus.types.ordering import PlaylistOrdering
from ymp.dbus.types.playback import PlaybackStatus
from ymp.dbus.types.metadata import Metadata
from ymp.dbus.types.loop import LoopStatus
from ymp.backend import Backend
from ymp.lib import vlc

import dbus


# TODO signals


class VLCBackend(Backend):
    def __init__(self, loop):
        self.loop = loop

        self.instance = vlc.Instance('--no-video')
        self.player = self.instance.media_player_new()

        self._loop_status = LoopStatus.PLAYLIST
        self._shuffle = True

    def can_quit(self):
        return True

    def fullscreen(self, arg=None):
        if arg is None:
            return bool(self.player.get_fullscreen())
        return

    def can_set_fullscreen(self):
        return False

    def can_raise(self):
        return False

    def raise_(self):
        pass

    def quit(self):
        self.loop.quit()

    def has_track_list(self):
        # TODO maybe
        return False

    def playback_status(self):
        state = self.player.get_state()
        return {
            vlc.State.Paused: PlaybackStatus.PAUSED,
            vlc.State.Playing: PlaybackStatus.PLAYING
        }.get(state, PlaybackStatus.STOPPED)

    def loop_status(self, arg=None):
        if arg is None:
            return self._loop_status
        self._loop_status = LoopStatus(arg)

    def rate(self, arg=None):
        # TODO player.get_rate/set_rate
        if arg is None:
            return 1.0

    def shuffle(self, arg=None):
        if arg is None:
            return self._shuffle
        self._shuffle = arg

    def metadata(self):
        # TODO
        return Metadata()

    def volume(self, arg=None):
        if arg is None:
            return max(min(self.player.audio_get_volume() / 100.0, 0), 1.0)
        self.player.audio_set_volume(min(max(0, arg*100.0), 100))

    def position(self):
        # TODO check value
        return dbus.Int64(max(self.player.get_time()*1000, 0))

    def minimum_rate(self):
        # TODO
        return 1.0

    def maximum_rate(self):
        # TODO
        return 1.0

    def can_go_next(self):
        # TODO
        return True

    def can_go_previous(self):
        # TODO
        return True

    def can_play(self):
        return bool(self.player.will_play())

    def can_pause(self):
        return bool(self.player.can_pause())

    def can_seek(self):
        return bool(self.player.is_seekable())

    def can_control(self):
        return True

    def next(self):
        # TODO
        pass

    def previous(self):
        # TODO
        pass

    def pause(self):
        self.player.set_pause(1)

    def play_pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def play(self):
        self.player.play()

    def seek(self, position):
        self.player.set_time(self.player.get_time() + position*1000)

    def set_position(self, trackid, position):
        # TODO trackid, check can seek
        self.player.set_time(position*1000)

    def open_uri(self, uri):
        # TODO
        pass

    def playlist_count(self):
        # TODO
        return 0

    def orderings(self):
        # TODO
        return [PlaylistOrdering.USER_DEFINED]

    def active_playlist(self):
        # TODO
        return MaybePlaylist(False, '/invalid', '', '')

    def activate_playlist(self, playlistid):
        # TODO
        pass

    def get_playlists(self, index, max_count, order, reversed_):
        # TODO
        return []

    def tracks(self):
        return []

    def can_edit_track(self):
        return False

    def get_tracks_metadata(self, trackids):
        return []

    def add_track(self, uri, after_track, set_as_current):
        pass

    def remove_track(self, trackid):
        pass

    def goto(self, trackid):
        pass
