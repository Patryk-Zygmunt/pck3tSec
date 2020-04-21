from django.db import models
from rest.enum_classes import ThreatType


class Host(models.Model):
    fqd_name = models.CharField(max_length=255, unique=True)
    blocked = models.BooleanField(default=False)
    original_ip = models.CharField(max_length=15, blank=True)
    is_threat = models.BooleanField(default=False)
    # TODO move this field to stats
    #last_accessed = models.DateTimeField(
     #   help_text="when HOST has been accessed recently, meaning there was net traffic with this host")


class Threat(models.Model):
    threat_type = models.CharField(choices=[(th.value, th.value.lower()) for th in ThreatType],  max_length=20)
    threat_details = models.TextField()
    http_path = models.CharField(max_length=2048, default="")
    discovered = models.DateTimeField()
    host_source = models.ForeignKey(Host, on_delete=models.CASCADE, null=False)

