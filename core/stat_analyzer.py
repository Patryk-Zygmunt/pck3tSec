from core.abstracts import IAnalyzer, IObservable, IObserver
from core.hostAnalyzer import HostAnalyzer
from typing import Optional
from scapy.layers import inet


class StatAnalyzer(IAnalyzer, IObservable):

    def __init(self):
        self.observers = []

    def register_observer(self, observer: IObserver):
        self.observers.append(observer)

    def get_ip_layer(self, packet) -> Optional[inet.IP]:
        if packet.haslayer(inet.IP):
            return packet.getlayer(inet.IP)

    def analyze(self, packet):
        ip_layer = self.get_ip_layer(packet)
        if ip_layer:
                 pass