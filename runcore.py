import sys, os, logging

cwd = os.getcwd()
api_path = os.path.join(cwd, 'api')
core_path = os.path.join(cwd, 'core')
sys.path.append(core_path)
sys.path.append(api_path)


from django_external_setup import django_external_setup
from analyzeDispatcher import AnalyzeDispatcher
from googleSafeBrowsing import GoogleSafeBrowsing
from hostAnalyzer import HostAnalyzer
from packetReader import PacketReader
from api.settings import LOGGING

if __name__ == '__main__':
    print("Warinig! this script needs root privileges")
    django_external_setup()
    logging.config.dictConfig(LOGGING)
    google_safe = GoogleSafeBrowsing("AIzaSyDyYREKVRoPgXSFvcRZuqFGZHlSFymDa80")
    analyzer1 = HostAnalyzer(google_safe)
    reader = PacketReader('en0')
    dispatcher = AnalyzeDispatcher(reader)
    dispatcher.register_analyzer(analyzer1)
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        dispatcher.finish()
