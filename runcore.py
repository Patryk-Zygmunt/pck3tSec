import sys, os, logging, pathlib

def config_paths():
    cwd = pathlib.Path(__file__).parent.absolute()
    api_path = os.path.join(str(cwd), 'api')
    sys.path.append(api_path)


config_paths()



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
