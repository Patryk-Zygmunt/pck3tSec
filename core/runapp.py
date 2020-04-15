from analyzeDispatcher import AnalyzeDispatcher
from googleSafeBrowsing import GoogleSafeBrowsing
from hostAnalyzer import HostAnalyzer
from packetReader import PacketReader

if __name__ == '__main__':

    google_safe = GoogleSafeBrowsing("AIzaSyDyYREKVRoPgXSFvcRZuqFGZHlSFymDa80")
    analyzer1 = HostAnalyzer(google_safe)
    reader = PacketReader('en0')
    dispatcher = AnalyzeDispatcher(reader)
    dispatcher.register_analyzer(analyzer1)
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        dispatcher.finish()
