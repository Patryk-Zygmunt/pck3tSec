from rest_framework import serializers
from rest import models
from rest.enum_classes import ListColor
import sys
from rest.host_blocker import HostBlocker


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = serializers.ALL_FIELDS


class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Threat
        fields = serializers.ALL_FIELDS
        depth = 1


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stats
        fields = serializers.ALL_FIELDS
        depth = 1


class BlackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManageList
        fields = ['id', 'host', 'reason', 'time_added']

    def validate_color(self, value):
        if value != ListColor.BLACK.value:
            raise serializers.ValidationError('It is not blacklist entry')
        return value

    def create(self, validated_data):
        blocker = HostBlocker()
        query = models.Host.objects.filter(id=validated_data['host'].id)
        if query.exists():
            host = query.get()
            host.blocked = True
            host.save()
            blocker.block_host(host.original_ip)
        return models.ManageList.objects.create(host_id=validated_data['host'].id,
                                                reason=validated_data['reason'],
                                                color=ListColor.BLACK.value)

