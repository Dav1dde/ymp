from ymp.dbus.types.playlist import Playlist, MaybePlaylist
from ymp.dbus.types.ordering import PlaylistOrdering
from ymp.dbus.types.playback import PlaybackStatus
from ymp.dbus.types.metadata import Metadata
from ymp.dbus.types.loop import LoopStatus
from ymp.backend import Backend
from ymp.lib import vlc

from gi.repository import GObject
import dbus


# TODO:
#  * trigger song url download for every next song asynchronously
#  * maybe figure out why seeking backwards doesn't work in mp4 audio streams

def _vlc_detach_all_events(em):
    for k, cb in em._callbacks.copy().items():
        em.event_detach(vlc.EventType(k))


def vlc_state_to_mpris_state(state):
    return {
        vlc.State.Paused: PlaybackStatus.PAUSED,
        vlc.State.Playing: PlaybackStatus.PLAYING
    }.get(state, PlaybackStatus.STOPPED)


class VLCBackend(Backend):
    def __init__(self, loop, provider, options=''):
        Backend.__init__(self)

        self.loop = loop
        self.provider = provider

        self.options = options
        if '--no-video' not in self.options:
            self.options = '--no-video {}'.format(self.options.strip())

        self.instance = vlc.Instance(self.options)
        self.player = self.instance.media_player_new()

        self._loop_status = LoopStatus.PLAYLIST
        self._shuffle = True

        self._is_stopped = True
        self._has_media = False

        # in heisenbugs we trust
        # we need to keep references of event managers
        # or else shit will go down
        self._vlc_player_event_manager = None
        self._vlc_media_event_manger = None

        # *NO* calls to vlc from callbacks!
        self._vlc_player_event_manager = self.player.event_manager()
        self._vlc_player_event_manager.event_attach(
            vlc.EventType.MediaPlayerSeekableChanged,
            lambda e: self.emit_notification('CanSeek', bool(e.u.new_seekable))
        )
        self._vlc_player_event_manager.event_attach(
            vlc.EventType.MediaPlayerPausableChanged,
            lambda e: self.emit_notification(
                'CanPause', bool(e.u.new_pausable) or self._is_stopped
            )
        )
        self._vlc_player_event_manager.event_attach(
            vlc.EventType.MediaPlayerMediaChanged,
            lambda e: self.emit_notification('Metadata', self.metadata())
        )
        self._vlc_player_event_manager.event_attach(
            vlc.EventType.MediaPlayerStopped,
            self.on_media_stopped,
        )
        self._vlc_player_event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached,
            self.on_media_end_reached
        )

        self.emit_notification('PlaybackStatus', PlaybackStatus.STOPPED)

    # events
    # do *NOT* make calls to vlc from callbacks!
    def on_media_end_reached(self, event):
        def advance():
            if self.can_go_next():
                self.next()

        # we want advance to be called from the main thread
        GObject.main_context_default().invoke_full(0, advance)

        return False

    def on_media_stopped(self, event):
        self._is_stopped = True
        self.emit_notification('PlaybackStatus', PlaybackStatus.STOPPED)

        self.emit_notification('CanPlay', self._has_media)
        self.emit_notification('CanPause', False)

    # other stuff
    def can_quit(self):
        return True

    def fullscreen(self, arg=None):
        if arg is None:
            return self.player.get_fullscreen() == 1
        self.emit_notification(self.fullscreen())
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
        return False  # TODO maybe

    def playback_status(self):
        state = self.player.get_state()
        return vlc_state_to_mpris_state(state)

    def loop_status(self, arg=None):
        if arg is None:
            return self._loop_status
        self._loop_status = LoopStatus(arg)
        self.emit_notification('LoopStatus')

    def rate(self, arg=None):
        # TODO player.get_rate/set_rate
        if arg is None:
            return 1.0

    def shuffle(self, arg=None):
        if arg is None:
            return self.provider.shuffle
        self.provider.shuffle = bool(arg)
        self.emit_notification('Shuffle')

    def metadata(self):
        if self.provider.current_song is None:
            return Metadata()
        return self.provider.current_song.metadata

    def volume(self, arg=None):
        if arg is None:
            return max(min(self.player.audio_get_volume() / 100.0, 0), 1.0)
        self.player.audio_set_volume(min(max(0, arg*100.0), 100))
        self.emit_notification('Volume')

    def position(self):
        return dbus.Int64(max(self.player.get_time()*1000, 0))

    def minimum_rate(self):
        return 1.0  # TODO

    def maximum_rate(self):
        return 1.0  # TODO

    def can_go_next(self):
        return self.provider.can_go_next()

    def can_go_previous(self):
        return self.provider.can_go_previous()

    def can_play(self):
        if self._is_stopped and self._has_media:
            return True
        return self.player.will_play() == 1

    def can_pause(self):
        # return self.player.is_playing() == 1
        return self.player.can_pause() == 1 and self.player.is_playing() == 1

    def can_seek(self):
        return self.player.is_seekable() == 1

    def can_control(self):
        return True

    def next(self):
        song = self.provider.next()
        self.open_uri(song.uri)
        self.play()

    def previous(self):
        song = self.provider.previous()
        self.open_uri(song.uri)
        self.play()

    def pause(self):
        self.player.set_pause(1)
        self._is_stopped = False

    def play_pause(self):
        if self._is_stopped and self._has_media:
            # explicitly play if stopped, or else vlc won't start playback
            return self.play()
        self.player.pause()
        self._is_stopped = False

    def stop(self):
        self.player.stop()
        self._is_stopped = True
        if self.provider.current_playlist is not None:
            self.provider.activate_playlist(self.provider.current_playlist.id)

    def play(self):
        self.player.play()
        self._is_stopped = False

    def seek(self, position):
        new_pos = max(self.player.get_time() + int(position/1000), 0)
        if new_pos > self.player.get_length():
            return self.next()

        self.player.set_time(new_pos)
        self.emit_event('seeked')

    def set_position(self, trackid, position):
        position = int(position/1000)
        if position < 0 or position > self.player.get_length():
            return

        if trackid == self.provider.current_song.id and self.can_seek():
            self.player.set_time(position)
            self.emit_event('seeked')

    def open_uri(self, uri):
        if self._vlc_media_event_manger is not None:
            _vlc_detach_all_events(self._vlc_media_event_manger)

        self._is_stopped = True
        self._has_media = True

        media = self.player.set_mrl(uri)

        em = media.event_manager()
        em.event_attach(
            vlc.EventType.MediaStateChanged,
            lambda e: self.emit_notification(
                'PlaybackStatus', vlc_state_to_mpris_state(e.u.new_status)
            )
        )
        self._vlc_media_event_manger = em

        self.emit_notification('CanPlay')
        self.emit_notification('CanPause')
        self.emit_notification('CanGoNext')
        self.emit_notification('CanGoPrevious')
        self.emit_notification('Metadata')

    def playlist_count(self):
        return len(self.provider.playlists)

    def orderings(self):
        # we take it as we get it from youtube/grooveshark, whatever
        return [PlaylistOrdering.USER_DEFINED]

    def active_playlist(self):
        return self.provider.current_playlist.dbus_playlist

    def activate_playlist(self, playlistid):
        self.provider.activate_playlist(playlistid)
        self.open_uri(self.provider.current_song.uri)
        self.play()

    def get_playlists(self, index, max_count, order, reversed_):
        return self.provider.dbus_playlists  # TODO args

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
