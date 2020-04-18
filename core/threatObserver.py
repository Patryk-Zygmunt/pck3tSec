import datetime
from abstracts import IObserver
from django_external_setup import django_external_setup
from rest.enum_classes import ThreatType


class ThreatObserver(IObserver):

    def __init__(self):
        django_external_setup()
        # can only be imported when django setup done
        from rest.models import Host, Threat


    def update(self, *args, **kwargs):
        threat_data = kwargs['data']


if __name__ == '__main__':
    import django_external_setup
    django_external_setup.django_external_setup()
    from rest.models import Host
    data = {'id': 1, 'is_threat': True, 'fqd_name': "kaczki.com", "last_accessed": datetime.datetime.now()}
    db_host = Host(**data)
    db_host.save()
    print(Host.objects.all())