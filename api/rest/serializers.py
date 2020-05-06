from rest_framework import serializers
from rest import models
from rest.enum_classes import ListColor


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


# class ManageListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ManageList
#         fields = serializers.ALL_FIELDS
#         depth = 1


class BlackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManageList
        fields = serializers.ALL_FIELDS

    def validate_color(self, value):
        if value != ListColor.BLACK.value:
            raise serializers.ValidationError('It is not blacklist entry')
        return value

    def create(self, validated_data):
        print(validated_data)
        return models.ManageList.objects.create(host_id=validated_data['host'].id,
                                                reason=validated_data['reason'],
                                                color=ListColor.BLACK.value)

