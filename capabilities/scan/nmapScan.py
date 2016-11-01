from capability import *
import nmap
from scapy.all import *
import pprint

class scanNmap(Capability):

    def __init__(self, core):
        super(scanNmap, self).__init__(core)
        self.name = "Nmap"
        self.intro = GOOD + "Using Nmap module..."
        self.core = core
        self.options = {
                "host":     Option("host", "10.0.0.57", "host to scan", True),
                "ports":    Option("ports", "0-1000", "ports to scan", True),
                }
        self.help_text = "Use this to scan as you would in nmap."


    def launch(self):
        scanner = nmap.PortScanner()
        results = scanner.scan(self.get_value("host"), self.get_value("ports"))
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(results["nmap"])
        pp.pprint(results["scan"])
