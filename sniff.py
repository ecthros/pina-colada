from scapy.all import *
import logging
import thread
import time
import datetime

def log_packet():
    pass #TODO log packet in another thread so database communication is not a bottleneck

def cb(packet):
    # TODO decide what fields we want to pull out of the packet
    pass

def listen(timeout=5):
    while True:
        try:
            pkts = sniff(timeout=timeout)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            wrpcap('/home/aces/pinyapwn/packets/{0}.pcap'.format(st), pkts)
        except Exception as e:
            print "failure"
            print e
            #print pkts


def start_sniffing():
    try:
        thread.start_new_thread (listen, ())
    except Exception as e:
        print "Thread creation failed"
        print e

