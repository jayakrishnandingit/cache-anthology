from components.interfaces import CacheInterface
from components.exceptions import CacheEmptyError, CacheKeyError


class LRUNode(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return '(%s, %s)' % (self.key, self.value)


class LRULinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None

    def get_node_class(self):
        return LRUNode

    def create_node(self, key, value):
        Node = self.get_node_class()
        return Node(key, value)

    def insert_at_front(self, node):
        if self.head is None:
            # cache is empty.
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_node(self, node):
        if self.head is None:
            raise Exception((
                f"Head node must not be NoneType to perform this operation."
                f" This is unexpected behaviour."))

        if node == self.head and node == self.tail:
            # only one item in cache.
            self.head = self.tail = None
        elif node == self.head:
            # remove node at the head.
            self.head = node.next
            self.head.prev = None
        elif node == self.tail:
            # remove tail node.
            self.tail = node.prev
            self.tail.next = None
        else:
            # remove a node in the middle.
            node.prev.next = node.next
            node.next.prev = node.prev


class LRUCache(CacheInterface, LRULinkedList):
    MAX_SIZE = 10

    def __init__(self):
        super().__init__()
        self.store = {}

    def __str__(self):
        return '%s' % self.store

    def set_max_size(self, new_size):
        self.MAX_SIZE = new_size

    @property
    def size(self):
        return len(self.store.keys())

    def set(self, key, value):
        if key not in self.store:
            if self.size == self.MAX_SIZE:
                # cache full. delete least recently used.
                self.delete(self.tail.key)
            node = self.create_node(key, value)
        else:
            node = self.store[key]
            node.value = value
            self.remove_node(node)

        self.insert_at_front(node)
        self.update_store(node.key, node)

    def get(self, key):
        if self.size == 0:
            raise CacheEmptyError()
        if key not in self.store:
            raise CacheKeyError(key)

        node = self.store[key]
        self.remove_node(node)
        self.insert_at_front(node)
        return node.value

    def delete(self, key):
        if self.size == 0:
            raise CacheEmptyError()
        if key not in self.store:
            raise CacheKeyError(key)

        node = self.store[key]        
        self.remove_node(node)
        self.store.pop(key)

    def update_store(self, key, node):
        self.store[key] = node
