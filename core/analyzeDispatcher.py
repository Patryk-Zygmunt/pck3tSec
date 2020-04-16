from core.packetReader import PacketReader
from core.analyzerBase import AnalyzerBase

class AnalyzeDispatcher:

    def __init__(self, reader: PacketReader):

        self.reader = reader
        self.analyzers = []

        self.active = True

    def register_analyzer(self, analyzer: AnalyzerBase):
        self.analyzers.append(analyzer)

    def run(self):
        # blocking
        if not self.reader.started():
            self.reader.sniff()
        while self.active:
            packets = self.reader.get_packets()
            for packet in packets:
                print(packet.summary())
                for analyzer in self.analyzers:
                    x = analyzer.analyze(packet)
                    if x:
                        print(x)
            self.reader.remove_old_packets()

    def finish(self):
        self.active = False
        self.reader.end()
