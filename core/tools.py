from scapy.all import IP, ICMP, sr1, conf
from typing import List, Tuple
import logging

logger = logging.getLogger()

def get_machine_live_ifaces() -> List[Tuple[str, str]]:
    """
    Get live intefraces of the machine - that have gateway and pass ping to 1.1.1.1
    returns: list of live interfaces with tuples: (interface_name, interface_ip)
    """
    IFACE_INDEX, IP_INDEX = 3, 4
    ifaces = conf.route.routes
    own_ifaces = [(x[IFACE_INDEX], x[IP_INDEX]) for x in ifaces if x[2] != '0.0.0.0']
    live = []
    for face in own_ifaces:
        icmp = IP(dst='1.1.1.1') / ICMP()
        # IP defines the protocol for IP addresses
        # dst is the destination IP address
        # TCP defines the protocol for the ports
        resp = sr1(icmp, timeout=5)
        if resp:
            live.append(face)
    return live


if __name__ == '__main__':
    x = get_machine_live_ifaces()
    print(x)
