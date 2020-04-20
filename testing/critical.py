import time
import requests
import logging
import threading
from core.tools import *
from runcore import prepare_app
from abc import ABC, abstractmethod
from rest.models import Host, Threat
import queue

logger = logging.getLogger()


class CriticalTest(ABC):

    def __init__(self):
        self.live_interface = get_machine_live_ifaces()
        self.app_thread = threading.Thread(target=self._run_core)
        self.dispatcher = None

    def _prep(self):
        self.dispatcher = prepare_app(self.live_interface[0][0])

    def _run_core(self):
        self.dispatcher.run()

    def start_app_threat(self):
        self.app_thread.start()

    def stop_app_threat(self):
        self.dispatcher.finish()
        self.app_thread.join()

    def _wait_for_live_app(self, timeout=15):
        t0 = time.time()
        while not self.dispatcher.active:
            time.sleep(0.2)
            if time.time() - t0 > timeout:
                raise TimeoutError

    @abstractmethod
    def _test(self):
        pass

    def perform_test(self):
        try:
            self._prep()
            self.start_app_threat()
            self._wait_for_live_app()
            self._test()
            self.stop_app_threat()
        except KeyboardInterrupt:
            self.stop_app_threat()


class HostThreatTest(CriticalTest):

    def __init__(self):
        # does not see https - only http ( because of paths)
        self.test_url = "http://testsafebrowsing.appspot.com/s/malware.html"
        super().__init__()

    def _test(self):
        logger.info("running host threat rest")
        res = requests.get(self.test_url)
        assert res.status_code == 200, "request fail"


if __name__ == '__main__':
    import os,sys, pathlib
    pwd = os.getcwd()
    path = pathlib.Path(pwd)
    print(sys.path)

    # threat_test = HostThreatTest()
    # threat_test.perform_test()

