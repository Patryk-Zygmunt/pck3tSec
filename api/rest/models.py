from django.db import models
from rest.enum_classes import ThreatType, ListColor


class Host(models.Model):
    fqd_name = models.CharField(max_length=255, unique=True)
    blocked = models.BooleanField(default=False)
    original_ip = models.CharField(max_length=15, blank=True)
    is_threat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Threat(models.Model):
    threat_type = models.CharField(choices=[(th.value, th.value.lower()) for th in ThreatType],  max_length=20)
    threat_details = models.TextField()
    http_path = models.CharField(max_length=2048, default="")
    discovered = models.DateTimeField()
    host_source = models.ForeignKey(Host, on_delete=models.CASCADE, null=False)


class Stats(models.Model):
    host_source = models.OneToOneField(Host, on_delete=models.CASCADE)
    ppm = models.FloatField(help_text="average packets per minute, may be empty", null=True)
    last_accessed = models.DateTimeField(
        help_text="when HOST has been accessed recently, meaning there was net traffic with this host")


class ManageList(models.Model):
    host = models.OneToOneField(Host, on_delete=models.CASCADE)
    reason = models.CharField(max_length=1024, blank=True)
    time_added = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=5, choices=[(col.value, col.value.lower()) for col in ListColor])
