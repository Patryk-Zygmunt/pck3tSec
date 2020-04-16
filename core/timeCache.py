from typing import Hashable
import datetime


class TimeCache:
     # TODO finish
    def __init__(self, keep_time: datetime.timedelta, max_size=512):
        """
        TODO  separately update each filed - delete when to old
        Underling structure is mapping of hasable object to time it got added in ms
        For now just clear cache after oldest timestampt is bigger than durancy
        :param cacheing_durancy: store time in minutes
        :param max_size: maximum numer of cached objects
        """

        self.cache = {}
        self.keep_time = keep_time
        self.max_size = max_size

    def __contains__(self, item: Hashable) -> bool:
        self._update_cache()
        return item in self.cache

    def add(self, item: Hashable):
        self._update_cache()
        if not self.__contains__(item):
            self.cache[item] = datetime.datetime.now()

    def _update_cache(self):
        if self.cache:
            max_time = max(self.cache.values())
            timeout = datetime.datetime.now() - max_time >= self.keep_time
            maxout = len(self.cache) > self.max_size
            if timeout or maxout:
                self.cache.clear()
