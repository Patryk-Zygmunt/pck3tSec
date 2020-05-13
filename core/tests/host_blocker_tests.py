import unittest
from rest.host_blocker import HostBlocker
from unittest.mock import patch, call


class HostBlockerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_ip = '1.1.1.1'
        cls.output_table = b"""Chain OUTPUT (policy ACCEPT)
num  target     prot opt source               destination         
1    REJECT     all  --  0.0.0.0/0            1.1.1.1              reject-with icmp-port-unreachable
"""
        cls.input_table = b"""Chain INPUT (policy ACCEPT)
num  target     prot opt source               destination         
1    ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           
2    DROP       all  --  1.1.1.1              0.0.0.0/0           
"""

    def setUp(self) -> None:
        self.blocker = HostBlocker()

    def test_block_host_invalid_inp(self):
        with self.assertRaises(ValueError):
            self.blocker.block_host("ducks")

    def test_unblock_host_invalid_inp(self):
        with self.assertRaises(ValueError):
            self.blocker.unblock_host("ducks")

    def test_block_host(self):
        proper_call_sequence = [call(['/sbin/iptables', '-A', 'INPUT', '-s', self.test_ip, '-j', 'DROP'], check=True),
                                call(['/sbin/iptables', '-A', 'OUTPUT', '-d', self.test_ip, '-j', 'REJECT'], check=True),
                                call(['/sbin/iptables-save'], check=True)]
        with patch('subprocess.run') as run_mock:
            self.blocker.block_host(self.test_ip)
        calls = run_mock.mock_calls
        self.assertEqual(calls, proper_call_sequence)

    @patch('subprocess.run')
    def test_unblock_host(self,  mock_run):
        proper_call = [call(['/sbin/iptables', '-D', 'OUTPUT', '1']),
                        call(['/sbin/iptables', '-D', 'INPUT', '2']),
                        call(['/sbin/iptables-save'], check=True)]

        with patch('subprocess.check_output') as check_out_mock:
            check_out_mock.side_effect = [self.output_table, self.input_table]
            self.blocker.unblock_host(self.test_ip)
        self.assertEqual(check_out_mock.call_count, 2)
        self.assertEqual(mock_run.mock_calls, proper_call)
