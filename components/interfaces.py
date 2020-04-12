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


class LinkedListInterface(metaclass=ABCMeta):
    @abstractmethod
    def insert_at_front(self, node):
        pass

    @abstractmethod
    def delete_node(self, node):
        pass
