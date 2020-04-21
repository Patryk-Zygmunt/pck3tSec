from rest_framework import serializers
from rest import models


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = serializers.ALL_FIELDS


class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Threat
        fields = serializers.ALL_FIELDS
        depth = 1


