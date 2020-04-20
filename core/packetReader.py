import logging
from scapy.all import IPSession, AsyncSniffer, TCPSession, load_layer
from scapy.layers import http

logger = logging.getLogger()


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
        logger.debug('read packet {}'.format(packet.summary()))
        self.store.append(packet)

    def sniff(self, count=0):
        """
        start async sniffer
        """
        logger.info("starting to sniff packets")
         # TODO filter all outcoming packets
        self.sniffer = AsyncSniffer(session=TCPSession, prn=self._store, iface=self.interface, count=count, store=False)
        self.sniffer.start()

    def get_packets(self) -> list:
        """
        get new packets since last call of this function
        """
        logger.debug("getting new packets with index at {}".format(self.last_index))
        index = self.last_index
        self.last_index = len(self.store)
        logger.debug("new index is at {}".format(self.last_index))
        return self.store[index:]

    def end(self):
        logger.info("stopping reader")
        if not self.sniffer or not self.sniffer.running:
            logger.error("sniffer not started")
            raise Exception("first call sniff")
        return self.sniffer.stop()

    def remove_old_packets(self):
        """
        remove all already read packets by `get_packets`
        !! Warning - you will loose the references to those packets !!
        """
        logger.debug("removing old packets with index at {}".format(self.last_index))
        del self.store[:self.last_index]

    def started(self) -> bool:
        return True if self.sniffer else False

    def packet_q(self) -> int:
        """
        how many packets is currently in store, not processed
        """
        return len(self.store) - self.last_index


if __name__ == '__main__':
    load_layer('http')
    p = PacketReader('en0')
    p.sniff()
    while True:
        pck = p.get_packets()
        for pac in pck:
            if pac.haslayer(http.HTTP):
                print(pac.show())
