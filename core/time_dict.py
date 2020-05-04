import time
import logging
from collections import UserDict
from threading import Thread, Lock, Event
from datetime import timedelta, datetime
from collections import namedtuple
from typing import Dict, Callable, Any, List


logger = logging.getLogger()


class TimeDict(UserDict):
    TimedKey = namedtuple('TimedKey', ['time', 'key'])

    class Updater(Thread):
        def __init__(self, store: Dict, time_store: List,
                     lock: Lock, poll_time: float, action_time: timedelta, action, no_delete):
            super().__init__()
            self.store = store
            self.time_store = time_store
            self.lock = lock
            self.poll_time = poll_time
            self.action_time = action_time
            self.action = action
            self.no_delete = no_delete

            self.active = Event()
            self.removed_elems = 0
            self.exception = None

        def start(self) -> None:
            self.active.set()
            super().start()

        def flush(self):
            with self.lock:
                no_del_store = self.no_delete
                self.no_delete = True
                for tv in self.time_store:
                    self._handle_timed(tv)
                self.store.clear()
                self.time_store.clear()
                self.no_delete = no_del_store

        def join(self, *args, **kwargs):
            logger.info('stopping updater thread')
            self.active.clear()
            super().join(*args, **kwargs)

        def _handle_timed(self, obj):
            value = self.store[obj.key]
            if self.action:
                self.action(obj.key, value)
            if not self.no_delete:
                self.removed_elems += 1
                del self.store[obj.key]

        def _timestore_remove_old(self):
            # make sure last object does not stay
            # varying indexes, store as higher source of truth
            if self.removed_elems > 0:
                self.time_store[:] = self.time_store[self.removed_elems:]
                self.removed_elems = 0
            assert len(self.store) == len(self.time_store), "mismanaged object in store, len varies"

        def run(self):
            try:
                logger.info('updater thread started')
                while self.active.is_set():
                    time.sleep(self.poll_time)
                    now = datetime.now()
                    # TODO better optimize locking
                    self.lock.acquire()
                    for i, tv in enumerate(self.time_store):
                        if now - tv.time >= self.action_time:
                            self._handle_timed(tv)
                        else:
                            # list should be sorted descending with age of object ( assured by insertion )
                            # so if first or n-th object id not old enough all the following also won't be
                            break
                    self._timestore_remove_old()
                    self.lock.release()
            except Exception as e:
                self.exception = e
                if self.lock.locked():
                    self.lock.release()

    def __init__(self, action_time: timedelta, poll_time: float = 2, action: Callable[[Any, Any], None] = None,
                 no_delete=False):
        """
        Updating structure only updates the value but not the time- original insertion time is considered
        destroy method must be called remove this struct or it causes interpreter hangup at exit
        poll time should be around 1/4 of action time or less, to frequent polling is not recommened due to frequent
        mutex locking
        :param poll_time: is the frequency with which data will polled to check for timeouts,  value is in seconds
        :param action_time: is the age of object has to be (since insertion) for action to be taken
        :param action: action to be taken on object passing defined age - default is delete the object
                should be function that takes key, value as param and has no return value
                - `def action(key, value) ->None`
        :param no_delete: do not delete object after action() fired, default is False
        """
        super().__init__()
        self.lock = Lock()
        self.time_list = []
        self.updater = self.Updater(self.data, self.time_list, self.lock, poll_time, action_time, action, no_delete)
        self.updater.start()

    def _check_exception(self):
        """
        Check if updater thread is working, if not re raise exception
        """
        if self.updater.exception:
            raise self.updater.exception

    def clear(self) -> None:
        self._check_exception()
        with self.lock:
            self.time_list.clear()
            self.data.clear()

    def flush(self):
        """
        Does not respect object age, calls action method on all objects and clears them
        """
        self._check_exception()
        self.updater.flush()

    def destroy(self):
        self.updater.active.clear()

    def __setitem__(self, key, value):
        self._check_exception()
        with self.lock:
            if key not in self.data:
                tv = self.TimedKey(datetime.now(), key)
                self.time_list.append(tv)
            super().__setitem__(key, value)

    def __len__(self):
        with self.lock:
            return len(self.data)

    def __getitem__(self, key):
        self._check_exception()
        with self.lock:
            return super().__getitem__(key)

    def __contains__(self, key):
        self._check_exception()
        with self.lock:
            return super().__contains__(key)

    def __delitem__(self, key):
        """ This is slow operation - O(n)"""
        self._check_exception()
        with self.lock:
            value_index = [i for i, v in enumerate(self.time_list) if v.key == key].pop()
            del self.time_list[value_index]
            super().__delitem__(key)

    def __repr__(self):
        return self.data.__repr__() + "\n" + self.time_list.__repr__()

    def __del__(self):
        self.destroy()
        self.updater.join()

