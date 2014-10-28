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
    def __init__(self, loop, provider):
        self.loop = loop
        self.provider = provider

        self.instance = vlc.Instance('--no-video')
        self.player = self.instance.media_player_new()

        self._loop_status = LoopStatus.PLAYLIST
        self._shuffle = True

    def can_quit(self):
        return True

    def fullscreen(self, arg=None):
        if arg is None:
            return self.player.get_fullscreen() == 0
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
            return self.provider.shuffle
        self.provider.shuffle = bool(arg)

    def metadata(self):
        return self.provider.current_song.metadata

    def volume(self, arg=None):
        if arg is None:
            return max(min(self.player.audio_get_volume() / 100.0, 0), 1.0)
        self.player.audio_set_volume(min(max(0, arg*100.0), 100))

    def position(self):
        return dbus.Int64(max(self.player.get_time()*1000, 0))

    def minimum_rate(self):
        # TODO
        return 1.0

    def maximum_rate(self):
        # TODO
        return 1.0

    def can_go_next(self):
        # TODO
        return self.provider.can_go_next()

    def can_go_previous(self):
        # TODO
        return self.provider.can_go_previous()

    def can_play(self):
        return self.player.will_play() == 0

    def can_pause(self):
        return self.player.can_pause() == 0

    def can_seek(self):
        return self.player.is_seekable() == 0

    def can_control(self):
        return True

    def next(self):
        song = self.provider.next()
        self.player.set_mrl(song.uri)

    def previous(self):
        song = self.provider.previous()
        self.player.set_mrl(song.uri)

    def pause(self):
        self.player.set_pause(1)

    def play_pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def play(self):
        self.player.play()

    def seek(self, position):
        self.player.set_time(self.player.get_time() + position*100000)

    def set_position(self, trackid, position):
        # TODO trackid, check can seek
        self.player.set_time(position*100000)

    def open_uri(self, uri):
        # TODO disallow?
        self.player.set_mrl(uri)

    def playlist_count(self):
        return len(self.provider.playlists)

    def orderings(self):
        # we take it as we get it from youtube/grooveshark, whatever
        return [PlaylistOrdering.USER_DEFINED]

    def active_playlist(self):
        return self.provider.playlist.dbus_playlist

    def activate_playlist(self, playlistid):
        self.provider.activate_playlist(playlistid)
        self.player.set_mrl(self.provider.current_song.uri)

    def get_playlists(self, index, max_count, order, reversed_):
        return self.provider.dbus_playlists

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
