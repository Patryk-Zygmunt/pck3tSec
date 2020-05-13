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
import subprocess

logger = logging.getLogger()


class CriticalTest(ABC, TestCase):

    class AppThread(threading.Thread):

        def __init__(self, iface):
            super().__init__()
            self.dispatcher = prepare_app(iface)

        def run(self):
            self.dispatcher.run()

    def __init__(self, iface):
        TestCase.__init__(self)
        self.app_thread = self.AppThread(iface)

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

    def pre_test(self):
        dutils.setup_test_environment()
        old_conf = dutils.setup_databases(1, False)
        self.start_app_threat()
        self._wait_for_live_app()
        return old_conf

    def post_test(self, conf):
        self.stop_app_threat()
        dutils.teardown_databases(conf, 1)
        dutils.teardown_test_environment()
        subprocess.run(['/sbin/iptables', '-F', 'INPUT'])
        subprocess.run(['/sbin/iptables', '-F', 'OUTPUT'])

    def perform_test(self):
        try:
            db_conf = self.pre_test()
            self.test()
            self.post_test(db_conf)
        except KeyboardInterrupt:
            self.stop_app_threat()


class HostThreatTest(CriticalTest):

    def __init__(self, iface):
        # does not see https - only http ( because of paths)
        self.test_url = "http://testsafebrowsing.appspot.com/s/malware.html"
        super().__init__(iface)

    def test(self):
        logger.info("running host threat rest")
        res = requests.get(self.test_url)
        assert res.status_code == 200, "request fail"
        # wait to process request by app
        time.sleep(4)
        query = Threat.objects.filter(http_path=self.test_url[7:])
        logger.info("threat object is {}".format(query.get().__dict__))
        self.assertTrue(query.exists())
        logger.info("Threat test passed")


