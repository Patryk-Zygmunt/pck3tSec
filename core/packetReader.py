from scapy.all import IPSession, AsyncSniffer

class PacketReader:
    """
    This class needs root privileges to run
    """
    def __init__(self, interface: str):
        self.interface = interface
        self.store = []
        self.sniffer = None
        self.last_index = 0

    def _store(self, packet):
        self.store.append(packet)

    def sniff(self):
        """
        start async sniffer
        """
         # TODO filter all outcoming packets
        self.sniffer = AsyncSniffer(session=IPSession, prn=self._store, iface=self.interface)
        self.sniffer.start()

    def get_packets(self) -> list:
        """e
        get new packets since last call of this function
        """
        index = self.last_index
        self.last_index = len(self.store)
        return self.store[index:]

    def end(self):
        if not self.sniffer:
            raise Exception("first call sniff")
        self.sniffer.stop()

    def remove_old_packets(self):
        """
        remove all already read packets by `get_packets`
        !! Warning - you will loose the references to those packets !!
        """
        del self.store[:self.last_index]


