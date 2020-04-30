import logging
from core.abstracts import Analyzer, IObserver
from core.time_dict import TimeDict
from typing import Optional
from scapy.layers import inet, http
from rest.models import Host, Stats
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger()


class StatAnalyzer(Analyzer):

    def __init__(self):
        Analyzer.__init__(self)
        self.db_cache = TimeDict(action_time=timedelta(seconds=20), poll_time=5, action=self._handle_db_save)
        self.observers = []

    def register_observer(self, observer: IObserver):
        self.observers.append(observer)

    def finish(self):
        logger.info("stopping stat analyzer")
        self.db_cache.flush()
        self.db_cache.destroy()

    def _get_ip_layer(self, packet) -> Optional[inet.IP]:
        if packet.haslayer(inet.IP):
            return packet.getlayer(inet.IP)

    def get_hostname(self, packet, ip: str) -> Optional[str]:
        if packet.haslayer(http.HTTPRequest):
            return packet.getlayer(http.HTTPRequest).Host.decode('utf-8')
        return self.resolve_ip_to_hostname(ip)

    def _handle_db_save(self, hostname: str, ip: str):
        host, created = Host.objects.filter(fqd_name=hostname)\
            .get_or_create(
            fqd_name=hostname,
            original_ip=ip
        )
        # TODO bufor stats saves
        stat_query = Stats.objects.filter(host_source_id=host.id)
        if stat_query.exists():
            stat = stat_query.get()
            stat.last_accessed = timezone.now()
        else:
            stat = Stats(host_source_id=host.id, last_accessed=timezone.now())
        stat.save()
        if created:
            logger.info(f"new host added to db {hostname}")
        logger.info(f"stats updated on host {hostname}")

    def analyze(self, packet):
        ip_layer = self._get_ip_layer(packet)
        if ip_layer:
            ip = self._get_ip_of_foreign_host_bidirect(ip_layer)
            hostname = self.get_hostname(packet, ip)
            if hostname and not ip.endswith('255'):
                self.db_cache[hostname] = ip
            else:
                logger.info("hostname empty - skipping")