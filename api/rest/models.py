from django.db import models
from rest.enum_classes import ThreatType


class Host(models.Model):
    id = models.IntegerField(primary_key=True)
    fqd_name = models.CharField(max_length=255, unique=True)
    blocked = models.BooleanField(default=False)
    original_ip = models.CharField(max_length=15)
    is_threat = models.BooleanField(default=False)
    last_accessed = models.DateTimeField()


class Threat(models.Model):
    id = models.IntegerField(primary_key=True)
    threat_type = models.CharField(choices=[(th, th.value) for th in ThreatType], null=True, max_length=20)
    threat_details = models.TextField()
    http_path = models.CharField(max_length=2048, default="")
    discovered = models.DateTimeField()
    host_source = models.ForeignKey(Host, on_delete=models.CASCADE)

