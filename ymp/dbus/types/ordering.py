class PlaylistOrdering(str):
    VALUES = ('Alphabetical', 'CreationDate', 'ModifiedDate', 'LastPlayDate', 'UserDefined')

    def __init__(self, status, *args, **kwargs):
        if status not in self.VALUES:
            raise ValueError('Invalid LoopStatus "{}"'.format(status))

        str.__init__(status, *args, **kwargs)

    def __int__(self):
        return self.VALUES.index(self)

PlaylistOrdering.ALPHABETICAL = PlaylistOrdering('Alphabetical')
PlaylistOrdering.CREATION_DATE = PlaylistOrdering('CreationDate')
PlaylistOrdering.MODIFIED_DATE = PlaylistOrdering('ModifiedDate')
PlaylistOrdering.LAST_PLAY_DATE = PlaylistOrdering('LastPlayDate')
PlaylistOrdering.USER_DEFINED = PlaylistOrdering('UserDefined')
