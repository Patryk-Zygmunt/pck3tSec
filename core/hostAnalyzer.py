from googleSafeBrowsing import GoogleSafeBrowsing
from timeCache import TimeCache
from scapy.layers import http, inet
from abstracts import IAnalyzer, IObservable, IObserver
from scapy.all import conf
from typing import Optional, Tuple, Dict
from datetime import timedelta
import socket
import logging

logger = logging.getLogger(__name__)


class HostAnalyzer(IAnalyzer, IObservable):
    """
    for now we are onyl considering destination hosts for ip packets and
    host/path for http layer
    """

    def __init__(self, google_safe: GoogleSafeBrowsing):
        self.safe_browsing = google_safe
        self.own_interfaces = self._get_own_interfaces()

        self.safe_cache = TimeCache(timedelta(minutes=30))
        self.observers = []

    def register_observer(self, observer: IObserver):
        logger.info("registering observer {}".format(observer.__class__.__name__))
        self.observers.append(observer) 

    def notify(self, *args, **kwargs):
        for observer in self.observers:
            logger.info("notyfing observer {}".format(observer.__class__.__name__))
            observer.update(*args, **kwargs)

    def _get_own_interfaces(self) -> list:
        """
        get interface with ips for that which has gateway
        :return: list of ips of this machine that have gateways
        """
        ifaces = conf.route.routes
        own_ifaces = [x[4] for x in ifaces if x[2] != '0.0.0.0']
        logger.info(f"own interface is {own_ifaces}")
        return own_ifaces

    @staticmethod
    def resolve_ip_to_hostname(ips: str) -> Optional[str]:
        try:
            return socket.gethostbyaddr(ips)[0]
        except socket.herror:
            logger.warning(f"host could not be resolved for {ips}")

    def _get_ip_of_foreign_host(self, ip: inet.IP) -> Optional[str]:
        if ip.dst not in self.own_interfaces:
            return ip.dst

    def _handle_ip_layer(self, packet) -> Optional[str]:
        ip_packet = packet.getlayer(inet.IP)
        dst_host = self._get_ip_of_foreign_host(ip_packet)
        if dst_host:
            hostname = self.resolve_ip_to_hostname(dst_host)
            return hostname

    def _handle_http_layer(self, packet) -> Optional[str]:
        http_packet = packet.getlayer(http.HTTPRequest)
        host_path = f"{http_packet.Host}{http_packet.Path}"
        return host_path

    def is_host_safe(self, host: str) -> Tuple[bool, Dict]:
        ret_value = (True, {})
        if host not in self.safe_cache:
            logger.info(f"api call  for host {host}")
            ret_value = self.safe_browsing.api_call([host])
            if ret_value[0]:  # is safe
                logger.debug("host {} is safe".format(host))
                self.safe_cache.add(host)
            else:
                logger.info("host {} is threat, details: {}".format(host, ret_value[1]))
                self.notify(host, ret_value[1])
        return ret_value

    def analyze(self, packet):
        # TODO make it not return and comm with database
        host = None
        try:
            if packet.haslayer(http.HTTPRequest):
                logger.debug(f"packet {packet.summary()} has http layer")
                host = self._handle_http_layer(packet)
            elif packet.haslayer(inet.IP):
                logger.debug(f"packet {packet.summary()} has ip layer")
                host = self._handle_ip_layer(packet)
            if host:
                self.is_host_safe(host)
        except Exception:
            logger.exception(f"failed to check host for packet {packet.show}")
