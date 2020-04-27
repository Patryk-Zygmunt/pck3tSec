import time
import requests
import logging
import threading
import pathlib
import subprocess
import testing.mock_google_api
from core.analyzeDispatcher import AnalyzeDispatcher
from core.django_external_setup import django_external_setup
from core.googleSafeBrowsing import GoogleSafeBrowsing
from core.hostAnalyzer import HostAnalyzer
from core.packetReader import PacketReader
from core.threatObserver import ThreatObserver
from core.tools import *
from runcore import prepare_app
from abc import ABC, abstractmethod
from django.test import TestCase
from rest.models import Host, Threat
from unittest.mock import patch, PropertyMock, MagicMock
import django.test.utils as dutils
from api.settings import LOGGING


logger = logging.getLogger()


class CriticalTest(ABC, TestCase):

    @staticmethod
    def prepare_app_for_test(interface, google_safe):
        django_external_setup()
        logging.config.dictConfig(LOGGING)
        # threat analyzer
        analyzer1 = HostAnalyzer(google_safe)
        threat_observer = ThreatObserver()
        analyzer1.register_observer(threat_observer)

        reader = PacketReader(interface)
        dispatcher = AnalyzeDispatcher(reader)
        dispatcher.register_analyzer(analyzer1)
        return dispatcher

    class AppThread(threading.Thread):

        def __init__(self, is_ci):
            super().__init__()
            google_safe_api = GoogleSafeBrowsing("AIzaSyDyYREKVRoPgXSFvcRZuqFGZHlSFymDa80")
            if is_ci:
                self.interface = 'lo0'
                google_safe_api.url = "http://localhost:8123/googleapi/"
            else:
                self.interface = get_machine_live_ifaces()[0][0]
            self.dispatcher = CriticalTest.prepare_app_for_test(self.interface, google_safe_api)

        def run(self):
            self.dispatcher.run()

    def __init__(self, is_ci=False):
        TestCase.__init__(self)
        self.app_thread = self.AppThread(is_ci)



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
        finally:
            self.stop_app_threat()


class HostThreatTest(CriticalTest):

    def __init__(self, is_ci=False):
        # does not see https - only http ( because of paths)
        self.test_url = "http://testsafebrowsing.appspot.com/s/malware.html"
        super().__init__(is_ci=is_ci)
        self.is_ci = is_ci

    def _test(self):
        logger.info("running host threat rest")
        res = requests.get(self.test_url)
        assert res.status_code == 200, "request fail"
        # wait to process request by app
        time.sleep(4)
        query = Threat.objects.filter(http_path=self.test_url[len('http://'):])
        if self.is_ci:
            query = Threat.objects.all()
        logger.info("threat object is {}".format(query.get().__dict__))
        self.assertTrue(query.exists())
        logger.info("Threat test passed")


    def _run_mock_server(self):
        location = testing.mock_google_api.__file__
        path = pathlib.Path(location).absolute()
        print(f"path is {path}")
        server = subprocess.Popen(['python', path],)
        return server

    def test(self):
        server = None
        try:
            if self.is_ci:
                server = self._run_mock_server()
                self.test_url = "http://localhost:8123/s/malware/"
                print(f"server poll {server.poll()}")
                time.sleep(2)
            self._test()
        finally:
            if server:
                logger.info("stopping http server")
                server.terminate()

