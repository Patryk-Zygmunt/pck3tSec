import unittest
from core.time_cache import TimeCache
import datetime
import time


class TimeCacheTests(unittest.TestCase):
    keep_time = datetime.timedelta(seconds=0.5)

    def setUp(self) -> None:
        self.t_cache = TimeCache(keep_time=self.keep_time, max_size=2)
        self.test_obj = "some obj"

    def test_contains(self):
        self.t_cache.add(self.test_obj)
        self.assertTrue(self.test_obj in self.t_cache)

    def test_timeout_removal(self):
        self.t_cache.add(self.test_obj)
        time.sleep(0.6)
        res = self.test_obj in self.t_cache
        self.assertFalse(res)
        self.assertEqual(self.t_cache.cache, {})

    def test_size_removal(self):
        self.t_cache.add(self.test_obj)
        self.t_cache.add("test2")
        self.t_cache.add("test3")
        self.assertFalse(self.test_obj in self.t_cache)
        self.assertEqual(self.t_cache.cache, {})


if __name__ == '__main__':
    unittest.main()
