class LoopStatus(str):
    VALUES = ('None', 'Track', 'Playlist')

    def __init__(self, status, *args, **kwargs):
        if status not in self.VALUES:
            raise ValueError('Invalid LoopStatus "{}"'.format(status))

        str.__init__(status, *args, **kwargs)

    def __int__(self):
        return self.VALUES.index(self)

LoopStatus.NONE = LoopStatus('None')
LoopStatus.TRACK = LoopStatus('Track')
LoopStatus.PLAYLIST = LoopStatus('Playlist')