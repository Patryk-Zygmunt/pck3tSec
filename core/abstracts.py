from abc import ABC, abstractmethod
from typing import Optional, List
from scapy.layers import inet
from scapy.all import conf
import socket
import logging


logger = logging.getLogger()

class IObserver(ABC):

    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class IObservable(ABC):

    @abstractmethod
    def register_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass


class Analyzer(ABC):

    def __init__(self, own_iface: Optional[List[str]] = None):
        self.own_interfaces = own_iface
        if not own_iface:
            self.own_interfaces = self._get_own_interfaces()

    @abstractmethod
    def analyze(self, packet):
        pass

    def _get_own_interfaces(self) -> List[str]:
        """
        get interface with ips for that which has gateway
        :return: list of ips of this machine that have gateways
        """
        ifaces = conf.route.routes
        own_ifaces = [x[4] for x in ifaces if x[2] != '0.0.0.0']
        logger.info(f"own interface is {own_ifaces}")
        return own_ifaces

    def resolve_ip_to_hostname(self, ips: str) -> Optional[str]:
        try:
            return socket.gethostbyaddr(ips)[0]
        except socket.herror:
            logger.warning(f"host could not be resolved for {ips}")

    def _get_ip_of_foreign_host_outgoing(self, ip: inet.IP) -> Optional[str]:
        """
        return ip address if destination ip is not own address
        """
        if ip.dst not in self.own_interfaces:
            return ip.dst

    def _get_ip_of_foreign_host_bidirect(self, ip: inet.IP) -> str:
        """
        assume traffic is from or to app host
        return ip of packet that is not local ip - foreign ip
        """
        if ip.dst not in self.own_interfaces:
            return ip.dst
        elif ip.src not in self.own_interfaces:
            return ip.src
        else:
            return "0.0.0.0"
