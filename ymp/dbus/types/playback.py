class PlaybackStatus(str):
    VALUES = ('Playing', 'Paused', 'Stopped')

    def __init__(self, status, *args, **kwargs):
        if status not in self.VALUES:
            raise ValueError('Invalid LoopStatus "{}"'.format(status))

        str.__init__(status, *args, **kwargs)

    def __int__(self):
        return self.VALUES.index(self)

PlaybackStatus.PLAYING = PlaybackStatus('Playing')
PlaybackStatus.PAUSED = PlaybackStatus('Paused')
PlaybackStatus.STOPPED = PlaybackStatus('Stopped')
