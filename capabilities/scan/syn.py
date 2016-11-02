from capability import *
from scapy.all import *
import time
import datetime

class syn(Capability):

    def __init__(self, core):
        super(syn, self).__init__(core)
        self.name = "Syn Scan"
        self.intro = GOOD + "Using Syn Scan module..."
        self.core = core
        self.options = { 
                "target":   Option("target", "10.0.0.57", "target device to scan", True),
                "start":    Option("start", "0", "beginning port of scan", True),
                "end":      Option("end", "100", "ending port of range", True),
                }
        self.help_text = "Scans a computer on a specific port."

    def syn_scan(self, target, ports):
        ans,unans = sr(IP(dst=target)/TCP(dport=ports),timeout=.1,verbose=0)
        rep = []
        for s,r in ans:
            if not r.haslayer(ICMP):
                if r.payload.flags == 0x12:
                    rep.append(r.sprintf("%sport%"))
        for response in rep:
            print str(response) + " is open"

        print "Updating database..."
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        ports = ','.join(rep)
        self.core.cur.execute(" \
            UPDATE computers SET ip='{0}', ports='{1}', last_online='{2}' WHERE ip='{3}'; \
            INSERT INTO computers(ip,ports,last_online) SELECT '{4}', '{5}', '{6}' \
            WHERE NOT EXISTS (SELECT 1 FROM computers WHERE ip='{7}')" \
            .format(target, ports, st, target, target, ports, st, target))

        return rep

    def launch(self):
        self.syn_scan(self.get_value("target"), (int(self.get_value("start")), int(self.get_value("end"))))



