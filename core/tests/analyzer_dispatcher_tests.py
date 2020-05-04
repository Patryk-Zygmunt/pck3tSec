import unittest
from core.analyze_dispatcher import AnalyzeDispatcher
from unittest.mock import MagicMock


class AnalyzeDispatcherTests(unittest.TestCase):

    def setUp(self) -> None:
        self.packet_reader = MagicMock()
        self.dispatcher = AnalyzeDispatcher(self.packet_reader)

    def test_register_analyzer(self):
        analyzer = MagicMock()
        self.dispatcher.register_analyzer(analyzer)
        self.assertEqual(self.dispatcher.analyzers.pop(), analyzer)

    def test_finish(self):
        self.dispatcher.finish()
        self.assertFalse(self.dispatcher.active)
        self.packet_reader.end.assert_called_once()

    

