#This is the template to create backdoors. Please copy your backdoor into the suggested spots. Places you need to input are shown by ~tildes~.
from capability import *
from scapy.all import *
#Remember extra imports.

class syn(Capability):

    def __init__(self, core):
        super(syn, self).__init__(core)
        self.name = "Syn Scan"
        self.intro = GOOD + "Using Syn Scan module..."
        self.core = core
        self.options = { 
                "target":       Option("target", "", "target device to scan", True),
                "startPort":    Option("startPort", "", "Beginning port of scan", True),
                "endPort":      Option("endPort", "", "Ending port of range", True),
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
        return rep


    def launch(self):
        self.syn_scan(self.get_value("target"), (int(self.get_value("startPort")), int(self.get_value("endPort"))))



