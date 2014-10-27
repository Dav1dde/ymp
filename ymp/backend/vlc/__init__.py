from ymp.backend import Backend
from ymp.lib import vlc


class VLCBackend(Backend):
    def __init__(self):
        self.instance = vlc.Instance('--no-video')
        self.player = self.instance.media_player_new()
