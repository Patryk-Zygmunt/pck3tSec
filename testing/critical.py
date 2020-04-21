import time
import requests
import logging
import threading
from core.tools import *
from runcore import prepare_app
from abc import ABC, abstractmethod
from django.test import TestCase
from rest.models import Host, Threat
import django.test.utils as dutils

logger = logging.getLogger()


class CriticalTest(ABC, TestCase):

    class AppThread(threading.Thread):

        def __init__(self):
            super().__init__()
            self.dispatcher = prepare_app(get_machine_live_ifaces()[0][0])

        def run(self):
            self.dispatcher.run()

    def __init__(self):
        TestCase.__init__(self)
        self.live_interface = get_machine_live_ifaces()
        self.app_thread = self.AppThread()

    def start_app_threat(self):
        self.app_thread.start()

    def stop_app_threat(self):
        self.app_thread.dispatcher.finish()
        self.app_thread.join()

    def _wait_for_live_app(self, timeout=15):
        t0 = time.time()
        while not self.app_thread.dispatcher.active:
            time.sleep(0.2)
            if time.time() - t0 > timeout:
                raise TimeoutError

    @abstractmethod
    def test(self):
        pass


    def perform_test(self):
        try:
            dutils.setup_test_environment()
            old_conf = dutils.setup_databases(1, False)
            self.start_app_threat()
            self._wait_for_live_app()
            self.test()
            self.stop_app_threat()
            dutils.teardown_databases(old_conf, 1)
            dutils.teardown_test_environment()
        except KeyboardInterrupt:
            self.stop_app_threat()


class HostThreatTest(CriticalTest):

    def __init__(self):
        # does not see https - only http ( because of paths)
        self.test_url = "http://testsafebrowsing.appspot.com/s/malware.html"
        super().__init__()

    def test(self):
        logger.info("running host threat rest")
        res = requests.get(self.test_url)
        assert res.status_code == 200, "request fail"
        # wait to process request by app
        time.sleep(2)
        query = Threat.objects.filter(http_path=self.test_url[7:])
        print(query)
        self.assertTrue(query.exists())
        logger.info("Threat test passed")


