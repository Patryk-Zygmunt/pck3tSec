import unittest
from core.packetReader import PacketReader

class PacketReaderTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.reader = PacketReader('if0')

    def test_get_packets(self):
        mock_list = list(range(10))
        self.reader.store = mock_list
        self.assertEqual(self.reader.get_packets(), mock_list)
        self.assertEqual(self.reader.get_packets(), [])
        self.reader.store.extend([1,2,3])
        self.assertEqual(self.reader.get_packets(), [1,2,3])

    def test_remove_old_packets(self):
        mock_list = list(range(10))
        self.reader.store = mock_list
        self.reader.get_packets()
        short_list = [1,2,3]
        self.reader.store.extend(short_list)
        self.reader.remove_old_packets()
        self.assertEqual(self.reader.store, short_list)


if __name__ == '__main__':
    unittest.main()
