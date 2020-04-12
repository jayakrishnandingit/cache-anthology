import unittest

from adapter import CacheAdapter
from lru import LRUCache
from components.exceptions import CacheKeyError, CacheEmptyError


class CacheSetTestCase(unittest.TestCase):
    def setUp(self):
        self.ip_hits = CacheAdapter(cache=LRUCache())
        self.ip_hits.cache.set_max_size(3)

    def tearDown(self):
        self.ip_hits = None

    def test_empty_cache(self):
        self.assertIsNone(self.ip_hits.cache.head)
        self.assertIsNone(self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 0)
        self.ip_hits.set('192.168.1.1', 2)
        self.assertIsNotNone(self.ip_hits.cache.head)
        self.assertIsNotNone(self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.cache.head, self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 1)

    def test_cache_max_size_deletes_lru_item(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)
        self.ip_hits.set('192.168.1.4', 3)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.tail.value, 1)
        self.assertEqual(self.ip_hits.size, 3)

    def test_max_size_update_does_not_delete_lru_item(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)
        self.ip_hits.set('192.168.1.2', 4)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

    def test_update_item_moves_to_front(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.size, 3)
        self.ip_hits.set('192.168.1.2', 8)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.head.value, 8)
        self.assertEqual(self.ip_hits.size, 3)


class CacheGetTestCase(unittest.TestCase):
    def setUp(self):
        self.ip_hits = CacheAdapter(cache=LRUCache())
        self.ip_hits.cache.set_max_size(3)

    def tearDown(self):
        self.ip_hits = None

    def test_empty_cache(self):
        self.assertIsNone(self.ip_hits.cache.head)
        self.assertIsNone(self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 0)
        with self.assertRaises(CacheEmptyError):
            self.ip_hits.get('192.168.1.1')

    def test_invalid_key(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

        with self.assertRaises(CacheKeyError):
            self.ip_hits.get('192.168.1.4')

    def test_one_item_cache_is_success(self):
        self.assertIsNone(self.ip_hits.cache.head)
        self.assertIsNone(self.ip_hits.cache.tail)
        self.ip_hits.set('192.168.1.1', 2)
        self.assertEqual(self.ip_hits.cache.head, self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 1)

        self.ip_hits.get('192.168.1.1')
        self.assertEqual(self.ip_hits.cache.head, self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 1)

    def test_tail_item_moves_to_head(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

        self.ip_hits.get('192.168.1.1')
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.head.value, 2)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.tail.value, 1)
        self.assertEqual(self.ip_hits.size, 3)

    def test_head_remains_head(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

        self.ip_hits.get('192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

    def test_any_item_moves_to_head(self):
        self.ip_hits.cache.set_max_size(4)
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.ip_hits.set('192.168.1.4', 6)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.4')
        self.assertEqual(self.ip_hits.cache.head.value, 6)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 4)

        self.ip_hits.get('192.168.1.2')
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.head.value, 1)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 4)


class CacheDeleteTestCase(unittest.TestCase):
    def setUp(self):
        self.ip_hits = CacheAdapter(cache=LRUCache())
        self.ip_hits.cache.set_max_size(3)

    def tearDown(self):
        self.ip_hits = None

    def test_empty_cache(self):
        self.assertIsNone(self.ip_hits.cache.head)
        self.assertIsNone(self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 0)
        with self.assertRaises(CacheEmptyError):
            self.ip_hits.delete('192.168.1.1')

    def test_invalid_key(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

        with self.assertRaises(CacheKeyError):
            self.ip_hits.delete('192.168.1.4')

    def test_one_item_cache(self):
        self.assertIsNone(self.ip_hits.cache.head)
        self.assertIsNone(self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 0)
        self.ip_hits.set('192.168.1.1', 2)
        self.assertEqual(self.ip_hits.cache.head, self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 1)

        self.ip_hits.delete('192.168.1.1')
        self.assertIsNone(self.ip_hits.cache.head)
        self.assertIsNone(self.ip_hits.cache.tail)
        self.assertEqual(self.ip_hits.size, 0)

    def test_delete_head(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

        self.ip_hits.delete('192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.head.value, 1)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 2)

    def test_delete_tail(self):
        self.ip_hits.set('192.168.1.1', 2)
        self.ip_hits.set('192.168.1.2', 1)
        self.ip_hits.set('192.168.1.3', 5)
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.1')
        self.assertEqual(self.ip_hits.cache.tail.value, 2)
        self.assertEqual(self.ip_hits.size, 3)

        self.ip_hits.delete('192.168.1.1')
        self.assertEqual(self.ip_hits.cache.head.key, '192.168.1.3')
        self.assertEqual(self.ip_hits.cache.head.value, 5)
        self.assertEqual(self.ip_hits.cache.tail.key, '192.168.1.2')
        self.assertEqual(self.ip_hits.cache.tail.value, 1)
        self.assertEqual(self.ip_hits.size, 2)
