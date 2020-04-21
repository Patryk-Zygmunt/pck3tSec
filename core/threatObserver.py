import logging
from django.utils import timezone
from core.abstracts import IObserver
from core.django_external_setup import django_external_setup
from rest.enum_classes import ThreatType
from typing import Dict

django_external_setup()
from rest.models import Host, Threat

logger = logging.getLogger()


class ThreatObserver(IObserver):

    def _save_if_not_doubled(self, threat: Threat, source_host_id: int):
        query = Threat.objects.filter(threat_type=ThreatType.HOST, host_source=source_host_id)
        if query.exists():
            logger.info("Such threat entry already exists")
        else:
            logger.info("Threat saved in database")
            threat.save()

    def update(self, host: str, threat_details: Dict):
        http_path = host if '/' in host else ""
        host_name = host.split("/")[0]
        host_db, created = Host.objects.get_or_create(fqd_name=host_name, is_threat=True)

        db_threat = Threat(
            threat_type=ThreatType.HOST,
            threat_details=threat_details or "no details",
            http_path=http_path,
            discovered=timezone.now(),
            host_source=host_db
        )
        self._save_if_not_doubled(db_threat, host_db.id)


if __name__ == '__main__':
    to = ThreatObserver()
    to.update("ziomo", {})
