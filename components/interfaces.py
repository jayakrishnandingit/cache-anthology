from abc import ABCMeta, abstractmethod


class CacheInterface(metaclass=ABCMeta):
    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @property
    @abstractmethod
    def size(self):
        pass
