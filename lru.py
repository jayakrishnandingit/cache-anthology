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


class LRUCache(CacheInterface):
    MAX_SIZE = 10

    def __init__(self):
        self.store = {}
        self.head = None  # most recently used Node.
        self.tail = None  # least recently used Node.
        self.current_size = 0

    def __str__(self):
        return '%s' % self.store

    def set_max_size(self, new_size):
        self.MAX_SIZE = new_size

    def get_node_class(self):
        return LRUNode

    @property
    def size(self):
        return self.current_size

    def set(self, key, value):
        if key not in self.store:
            if self.size == self.MAX_SIZE:
                # cache full. delete least recently used.
                self.delete(self.tail.key)
            node = self._create_new_node(key, value)
        else:
            node = self.store[key]
            self.delete(node.key)
        self._move_to_front(node)
        self._update_store(node.key, node)
        self._incr_size()

    def get(self, key):
        if key not in self.store:
            raise CacheKeyError(key)

        node = self.store[key]
        # TODO: Wrong. Value goes missing.
        self.delete(node.key)
        self._move_to_front(node)
        return node.value

    def delete(self, key):
        if key not in self.store:
            raise CacheKeyError(key)

        node = self.store[key]        
        self._remove_node(node)
        self.store.pop(key)

    def _incr_size(self):
        assert self.size < self.MAX_SIZE
        self.current_size += 1

    def _decr_size(self):
        assert self.size > 0
        self.current_size -= 1

    def _remove_node(self, node):
        if self.size == 0:
            raise CacheEmptyError()

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
        self._decr_size()

    def _create_new_node(self, key, value):
        Node = self.get_node_class()
        return Node(key, value)

    def _move_to_front(self, node):
        if self.size == 0:
            # cache is empty.
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def _update_store(self, key, node):
        self.store[key] = node
