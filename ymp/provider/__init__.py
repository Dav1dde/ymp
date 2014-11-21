from ymp.provider.grooveshark import GroovesharkProvider
from ymp.provider.soundcloud import SoundCloudProvider
from ymp.provider.youtube import YoutubeProvider

from abc import ABCMeta, abstractclassmethod


class Provider(metaclass=ABCMeta):
    @abstractclassmethod
    def responsible_for(self, uri):
        pass

    @abstractclassmethod
    def load(self, playlist):
        pass
