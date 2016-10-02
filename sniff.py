from scapy.all import *
import logging
import threading

def log_packet():
    pass #TODO log packet in another thread so database communication is not a bottleneck

def cb(packet):
    # TODO decide what fields we want to pull out of the packet
    pass

def listen(filter=None, count=None):
    sniff(prn=cb)
