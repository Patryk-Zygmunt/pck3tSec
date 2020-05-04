from core.google_safe_browsing import GoogleSafeBrowsing
from core.time_cache import TimeCache
from scapy.layers import http, inet
from core.abstracts import Analyzer, IObservable, IObserver
from scapy.all import conf
from typing import Optional, Tuple, Dict
from datetime import timedelta
import socket
import logging


logger = logging.getLogger(__name__)


class HostAnalyzer(Analyzer, IObservable):
    """
    for now we are onyl considering destination hosts for ip packets and
    host/path for http layer
    """

    def __init__(self, google_safe: GoogleSafeBrowsing):
        Analyzer.__init__(self)
        self.safe_browsing = google_safe

        self.safe_cache = TimeCache(timedelta(minutes=30))
        self.observers = []

    def register_observer(self, observer: IObserver):
        logger.info("registering observer {}".format(observer.__class__.__name__))
        self.observers.append(observer) 

    def notify(self, *args, **kwargs):
        for observer in self.observers:
            logger.info("notifying observer {}".format(observer.__class__.__name__))
            observer.update(*args, **kwargs)

    def _handle_ip_layer(self, packet) -> Optional[str]:
        ip_packet = packet.getlayer(inet.IP)
        dst_host = self._get_ip_of_foreign_host_outgoing(ip_packet)
        if dst_host:
            hostname = self.resolve_ip_to_hostname(dst_host)
            return hostname

    def _handle_http_layer(self, packet) -> Optional[str]:
        http_packet = packet.getlayer(http.HTTPRequest)
        host = http_packet.Host.decode('utf-8')
        path = http_packet.Path.decode('utf-8')
        host_path = f"{host}{path}"
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
        logger.debug("host analyzer packet {}".format(packet.show))
        host = None
        if packet.haslayer(http.HTTPRequest):
            logger.debug(f"packet {packet.summary()} has http layer")
            host = self._handle_http_layer(packet)
        elif packet.haslayer(inet.IP):
            logger.debug(f"packet {packet.summary()} has ip layer")
            host = self._handle_ip_layer(packet)
        if host:
            self.is_host_safe(host)

    def finish(self):
        logger.info("stopping host analyzer")
