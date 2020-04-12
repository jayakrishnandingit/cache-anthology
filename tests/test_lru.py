import unittest

from adapter import CacheAdapter
from lru import LRUCache


class CacheSetTestCase(unittest.TestCase):
    def setUp(self):
        self.ip_hits = CacheAdapter(cache=LRUCache())
        self.ip_hits.cache.set_max_size(3)

    def tearDown(self):
        self.ip_hits = None

    def test_empty_cache(self):
        self.assertIsNone(self.ip_hits.cache.head)
        self.assertIsNone(self.ip_hits.cache.tail)
        self.ip_hits.set('192.168.1.1', 2)
        self.assertIsNotNone(self.ip_hits.cache.head)
        self.assertIsNotNone(self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.cache.head, self.ip_hits.cache.tail)

    def test_cache_max_size_deletes_lru_item(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.cache.size, 3)
        self.ip_hits.set('192.168.1.4', 3)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.tail.value, 1)
        self.assertEqual(self.ip_hits.cache.size, 3)

    def test_max_size_update_does_not_delete_lru_item(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.cache.size, 3)
        self.ip_hits.set('192.168.1.2', 4)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.cache.size, 3)

    def test_update_item_moves_to_front(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.size, 3)
        self.ip_hits.set('192.168.1.2', 8)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.head.value, 8)
        self.assertEqual(self.ip_hits.cache.size, 3)
