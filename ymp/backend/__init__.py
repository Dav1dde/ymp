from abc import ABCMeta, abstractclassmethod


class Backend(object, metaclass=ABCMeta):
    @abstractclassmethod
    def can_quit(self):
        pass

    @abstractclassmethod
    def fullscreen(self, arg=None):
        return

    @abstractclassmethod
    def can_set_fullscreen(self):
        pass

    @abstractclassmethod
    def can_raise(self):
        pass

    @abstractclassmethod
    def raise_(self):
        pass

    @abstractclassmethod
    def quit(self):
        pass

    @abstractclassmethod
    def has_track_list(self):
        pass

    @abstractclassmethod
    def playback_status(self):
        pass

    @abstractclassmethod
    def loop_status(self, arg=None):
        pass

    @abstractclassmethod
    def rate(self, arg=None):
        pass

    @abstractclassmethod
    def shuffle(self, arg=None):
        pass

    @abstractclassmethod
    def metadata(self):
        pass

    @abstractclassmethod
    def volume(self, arg=None):
        pass

    @abstractclassmethod
    def position(self):
        pass

    @abstractclassmethod
    def minimum_rate(self):
        pass

    @abstractclassmethod
    def maximum_rate(self):
        pass

    @abstractclassmethod
    def can_go_next(self):
        pass

    @abstractclassmethod
    def can_go_previous(self):
        pass

    @abstractclassmethod
    def can_play(self):
        pass

    @abstractclassmethod
    def can_pause(self):
        pass

    @abstractclassmethod
    def can_seek(self):
        pass

    @abstractclassmethod
    def can_control(self):
        pass

    @abstractclassmethod
    def next(self):
        pass

    @abstractclassmethod
    def previous(self):
        pass

    @abstractclassmethod
    def pause(self):
        pass

    @abstractclassmethod
    def play_pause(self):
        pass

    @abstractclassmethod
    def stop(self):
        pass

    @abstractclassmethod
    def play(self):
        pass

    @abstractclassmethod
    def seek(self, position):
        pass

    @abstractclassmethod
    def set_position(self, trackid, position):
        pass

    @abstractclassmethod
    def open_uri(self, uri):
        pass

    @abstractclassmethod
    def playlist_count(self):
        pass

    @abstractclassmethod
    def orderings(self):
        pass

    @abstractclassmethod
    def active_playlist(self):
        pass

    @abstractclassmethod
    def activate_playlist(self, playlistid):
        pass

    @abstractclassmethod
    def get_playlists(self, index, max_count, order, reversed_):
        pass

    @abstractclassmethod
    def tracks(self):
        pass

    @abstractclassmethod
    def can_edit_track(self):
        pass

    @abstractclassmethod
    def get_tracks_metadata(self, trackids):
        pass

    @abstractclassmethod
    def add_track(self, uri, after_track, set_as_current):
        pass

    @abstractclassmethod
    def remove_track(self, trackid):
        pass

    @abstractclassmethod
    def goto(self, trackid):
        pass


