import time

from scapy.all import IPSession, AsyncSniffer, TCPSession, load_layer
import scapy.layers.http as http

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

    def sniff(self, count=0):
        """
        start async sniffer
        """
         # TODO filter all outcoming packets
        self.sniffer = AsyncSniffer(session=TCPSession, prn=self._store, iface=self.interface, count=count, store=False)
        self.sniffer.start()

    def get_packets(self) -> list:
        """
        get new packets since last call of this function
        """
        index = self.last_index
        self.last_index = len(self.store)
        return self.store[index:]

    def end(self):
        if not self.sniffer or not self.sniffer.running:
            raise Exception("first call sniff")
        return self.sniffer.stop()

    def remove_old_packets(self):
        """
        remove all already read packets by `get_packets`
        !! Warning - you will loose the references to those packets !!
        """
        del self.store[:self.last_index]

    def started(self) -> bool:
        return True if self.sniffer else False

    def packet_q(self) -> int:
        """
        how many packets is currently in store, not processed
        """
        return len(self.store) - self.last_index


if __name__ == '__main__':
    #try:

        p = PacketReader('en0')
        p.sniff()
        import requests
        r = requests.get('http://wikipedia.org/wiki/Duck')
        print(r.status_code)
    #except KeyboardInterrupt:
   #     time.sleep(2)
        x = p.get_packets()
        for pc in x:
            #print(pc.show())
            if pc.haslayer(http.HTTPRequest):
                #print(pc.show())
                print(pc.getlayer(http.HTTPRequest).Path)
           # print(pc.haslayer(http.HTTPRequest))
        print(p.end())
