from rest_framework import generics
from rest.models import *
from rest.serializers import *


class HostListView(generics.ListAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class ThreatListView(generics.ListAPIView):
    queryset = Threat.objects.all()
    serializer_class = ThreatSerializer

class StatsListView(generics.ListAPIView):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
