import unittest
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from suggest.suggest import ThreadSafeMemoryCache


class TestThreadSafeMemoryCache(unittest.TestCase):

    def setUp(self):
        self.cache = ThreadSafeMemoryCache(max_size=5, ttl_seconds=1)

    def test_init(self):
        """Test initialization with different parameters."""
        cache1 = ThreadSafeMemoryCache()
        self.assertEqual(cache1.max_size, 1000)
        self.assertEqual(cache1.ttl, 3600)

        cache2 = ThreadSafeMemoryCache(max_size=10, ttl_seconds=60)
        self.assertEqual(cache2.max_size, 10)
        self.assertEqual(cache2.ttl, 60)

    def test_get_nonexistent(self):
        """Test get for non-existent key."""
        self.assertIsNone(self.cache.get("nonexistent"))

    def test_set_and_get(self):
        """Test setting and getting a value."""
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_update_existing(self):
        """Test updating existing key."""
        self.cache.set("key1", "value1")
        self.cache.set("key1", "updated_value")
        self.assertEqual(self.cache.get("key1"), "updated_value")

    def test_expiration(self):
        """Test that items expire after TTL."""
        cache = ThreadSafeMemoryCache(ttl_seconds=0.1)
        cache.set("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")

        # Wait for expiration
        time.sleep(0.2)
        self.assertIsNone(cache.get("key1"))

    def test_lru_eviction(self):
        """Test LRU eviction when cache reaches max size."""
        # Fill cache to capacity
        for i in range(5):
            self.cache.set(f"key{i}", f"value{i}")

        # All items should be in cache
        for i in range(5):
            self.assertEqual(self.cache.get(f"key{i}"), f"value{i}")

        # Add one more item, should evict the oldest (key0)
        self.cache.set("new_key", "new_value")
        self.assertIsNone(self.cache.get("key0"))
        self.assertEqual(self.cache.get("new_key"), "new_value")

        # Accessing key1 should move it to the end of the LRU queue
        self.assertEqual(self.cache.get("key1"), "value1")

        # Adding another item should now evict key2, not key1
        self.cache.set("another_key", "another_value")
        self.assertIsNone(self.cache.get("key2"))
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_clear(self):
        """Test clearing the cache."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")

        self.cache.clear()

        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))

    def test_remove_expired(self):
        """Test removing expired items."""
        cache = ThreadSafeMemoryCache(ttl_seconds=0.1)
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        # Wait for expiration
        time.sleep(0.2)

        # Add a fresh item
        cache.set("key3", "value3")

        # Remove expired items
        removed = cache.remove_expired()

        # Should have removed 2 items
        self.assertEqual(removed, 2)
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))
        self.assertEqual(cache.get("key3"), "value3")

    def test_thread_safety(self):
        """Test thread safety with concurrent operations."""
        num_threads = 50
        iterations = 100

        def worker():
            for i in range(iterations):
                # Add unique keys for each thread/iteration
                key = f"thread_{threading.get_ident()}_{i}"
                self.cache.set(key, i)

                # Random read (may or may not exist)
                self.cache.get(f"thread_{i % num_threads}_{i % iterations}")

        # Run concurrent workers
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker) for _ in range(num_threads)]

            # Wait for all to complete
            for future in futures:
                future.result()

        # If we got here without exceptions, the test passed
        # We would expect lock issues to cause exceptions

    def test_key_generation(self):
        """Test key generation logic."""
        key1 = self.cache._get_key("arg1", "arg2", kwarg1="value1")
        key2 = self.cache._get_key("arg1", "arg2", kwarg1="value1")
        key3 = self.cache._get_key("arg1", "arg2", kwarg1="different")

        # Same args should produce same key
        self.assertEqual(key1, key2)

        # Different args should produce different keys
        self.assertNotEqual(key1, key3)

        # Order of kwargs shouldn't matter
        key4 = self.cache._get_key("arg1", kwarg2="value2", kwarg1="value1")
        key5 = self.cache._get_key("arg1", kwarg1="value1", kwarg2="value2")
        self.assertEqual(key4, key5)
