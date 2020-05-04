from core.packet_reader import PacketReader
from core.abstracts import Analyzer
import logging

logger = logging.getLogger()


class AnalyzeDispatcher:

    def __init__(self, reader: PacketReader):

        self.reader = reader
        self.analyzers = []

        self.active = False

    def register_analyzer(self, analyzer: Analyzer):
        logger.info(f"registering analyzer {analyzer.__class__.__name__}")
        self.analyzers.append(analyzer)

    def run(self):
        # blocking
        logger.info("starting dispatcher")
        if not self.reader.started():
            self.reader.sniff()
        self.active = True
        while self.active:
            packets = self.reader.get_packets()
            for packet in packets:
                logger.debug("analyzing packet {}".format(packet.summary()))
                for analyzer in self.analyzers:
                    analyzer.analyze(packet)
            self.reader.remove_old_packets()

    def finish(self):
        logger.info("stopping dispatcher")
        self.active = False
        for analyzer in self.analyzers:
            analyzer.finish()
        self.reader.end()
