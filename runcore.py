from core.analyzeDispatcher import AnalyzeDispatcher
from core.googleSafeBrowsing import GoogleSafeBrowsing
from core.hostAnalyzer import HostAnalyzer
from core.packetReader import PacketReader

if __name__ == '__main__':
    print("Warinig! this script needs root privilages")
    google_safe = GoogleSafeBrowsing("AIzaSyDyYREKVRoPgXSFvcRZuqFGZHlSFymDa80")
    analyzer1 = HostAnalyzer(google_safe)
    reader = PacketReader('en0')
    dispatcher = AnalyzeDispatcher(reader)
    dispatcher.register_analyzer(analyzer1)
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        dispatcher.finish()