from django.test import TestCase
from django.urls import reverse
from rest.models import *
from rest.enum_classes import *
from django.utils import timezone
from rest_framework import status


class RESTTests(TestCase):

    host1 = {
        'fqd_name': 'ducks.com',
        'original_ip': '192.168.1.2',
    }
    host2 = {
        'fqd_name': 'cats.com',
        'original_ip': '123.154.154.1'
    }
    threat = {
        'threat_type': ThreatType.HOST.value,
        'threat_details': 'some detals',
        'http_path': '/abc/',
        'discovered': timezone.now(),
        'host_source_id': 1
    }
    stat = {
        'host_source_id': 2,
        'last_accessed': timezone.now()
    }
    blacklist = {
        'host_id': 1,
        'reason': 'some',
        'color': ListColor.BLACK.value
    }


    def setUp(self) -> None:
        h1 = Host.objects.create(**self.host1)
        Host.objects.create(**self.host2)
        Threat.objects.create(**self.threat)
        Stats.objects.create(**self.stat)
        ManageList.objects.create(**self.blacklist)
        h1.blocked = True
        h1.save()

    def test_get_hosts(self):
        url = reverse('api-hosts')
        res = self.client.get(url)
        self.assertEqual(2, len(res.json()))

    def test_get_threats(self):
        url = reverse('api-threats')
        res = self.client.get(url)
        self.assertEqual(1, len(res.json()))

    def test_get_stats(self):
        url = reverse('api-stats')
        res = self.client.get(url)
        self.assertEqual(1, len(res.json()))

    def test_post_blacklist(self):
        url = reverse('api-blacklists')
        res = self.client.post(url, {'host': 2, 'reason': 'some reason'})
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        host = Host.objects.get(id=2)
        self.assertTrue(host.blocked)

    def test_delete_blacklist(self):
        url = reverse('api-blacklist-item', args=(1,))
        res = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        host = Host.objects.get(id=1)
        self.assertFalse(host.blocked)

    def test_get_blacklist(self):
        url = reverse('api-blacklists')
        res = self.client.get(url)
        self.assertEqual(1, len(res.json()))
