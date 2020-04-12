class CacheAdapter(object):
    def __init__(self, cache):
        self.cache = cache

    def set(self, key, value):
        self.cache.set(key, value)

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        self.cache.delete(key)

    @property
    def size(self):
        return self.cache.size
