from abc import ABCMeta, abstractclassmethod


class Provider(metaclass=ABCMeta):
    @abstractclassmethod
    def responsible_for(self, uri):
        pass

    @abstractclassmethod
    def load(self, playlist):
        pass

    @staticmethod
    def all_providers():
        return Provider.__subclasses__()
