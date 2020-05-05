import re
import logging
import subprocess
from typing import Optional

logger = logging.getLogger()


class HostBlocker:
    IP_REGEX = re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

    def __init__(self):
        self.iptables = '/sbin/iptables'

    def _validate_host(self, host):
        if not self.IP_REGEX.match(host):
            raise ValueError('bad host format - should be IPv4')

    def _save_changes(self):
        subprocess.run([self.iptables+'-save'], check=True)

    def block_host(self, host_ip: str):
        self._validate_host(host_ip)
        logger.info(f'blocking host {host_ip}')
        command_ip_out = [self.iptables, '-A', 'OUTPUT', '-d', host_ip, '-j', 'REJECT']
        command_ip_in = [self.iptables, '-A', 'INPUT', '-s', host_ip, '-j', 'DROP']
        subprocess.run(command_ip_in, check=True)
        subprocess.run(command_ip_out, check=True)
        self._save_changes()

    def _find_rule_id_by_name(self, table: str, host_ip: str) -> Optional[int]:
        table = table.decode()
        logger.debug(f"iptable is {table}")
        spl = table.splitlines()
        content = spl[2:]
        for line in content:
            if host_ip in line and ('REJECT' in line or 'DROP' in line):
                return line[0]

    def unblock_host(self, host_ip: str):
        self._validate_host(host_ip)
        output_table = subprocess.check_output([self.iptables, '-L', 'OUTPUT', '-n', '--line-numbers'])
        input_table = subprocess.check_output([self.iptables, '-L', 'INPUT', '-n', '--line-numbers'])
        output_id = self._find_rule_id_by_name(output_table, host_ip)
        input_id = self._find_rule_id_by_name(input_table, host_ip)
        if output_id:
            logger.info(f'deleting rule from OUTPUT for ip {host_ip}')
            subprocess.run([self.iptables, '-D', 'OUTPUT', output_id])
        if input_id:
            logger.info(f'deleting rule form INPUT for ip {host_ip}')
            subprocess.run([self.iptables, '-D', 'INPUT', input_id])
        self._save_changes()


