from rest_framework import generics
from rest.models import *
from rest.serializers import *
from rest.enum_classes import ListColor


class HostListView(generics.ListAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class ThreatListView(generics.ListAPIView):
    queryset = Threat.objects.all()
    serializer_class = ThreatSerializer


class StatsListView(generics.ListAPIView):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer


class BlackListView(generics.ListCreateAPIView):
    queryset = ManageList.objects.filter(color=ListColor.BLACK.value)
    serializer_class = BlackListSerializer


class BlackListDetailView(generics.DestroyAPIView):
    queryset = ManageList.objects.filter(color=ListColor.BLACK.value)
    serializer_class = BlackListSerializer

    def perform_destroy(self, instance):
        host = Host.objects.get(id=instance.host_id)
        host.blocked = False
        host.save()
        super().perform_destroy(instance)
