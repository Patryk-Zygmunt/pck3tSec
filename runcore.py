import sys
import os
import logging

def config_paths():
    cwd = os.path.dirname(os.path.abspath(__file__))
    api_path = os.path.join(cwd, 'api')
    if api_path not in sys.path:
        sys.path.append(api_path)
    print(sys.path)


config_paths()

print(sys.path)

from core.django_external_setup import django_external_setup
from core.analyzeDispatcher import AnalyzeDispatcher
from core.googleSafeBrowsing import GoogleSafeBrowsing
from core.hostAnalyzer import HostAnalyzer
from core.packetReader import PacketReader
from core.threatObserver import ThreatObserver
from api.settings import LOGGING


def prepare_app(interface):
    django_external_setup()
    logging.config.dictConfig(LOGGING)
    # threat analyzer
    google_safe = GoogleSafeBrowsing("AIzaSyDyYREKVRoPgXSFvcRZuqFGZHlSFymDa80")
    analyzer1 = HostAnalyzer(google_safe)
    threat_observer = ThreatObserver()
    analyzer1.register_observer(threat_observer)

    reader = PacketReader(interface)
    dispatcher = AnalyzeDispatcher(reader)
    dispatcher.register_analyzer(analyzer1)
    return dispatcher


def main(interface):
    dispatcher = prepare_app(interface)
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        dispatcher.finish()


if __name__ == '__main__':
    print("Warinig! this script needs root privileges")
    main('en0')
