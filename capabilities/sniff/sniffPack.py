from scapy.all import *
import time
import datetime
import thread
import os
from capability import *

class sniffPack(Capability):

    def __init__(self, core):
        super(sniffPack, self).__init__(core)
        self.name = "Sniff"
        self.intro = GOOD + "Using Sniff module..."
        self.core = core
        self.options = { 
                "rate": Option("rate", "30", "number of seconds in between file writes", True),
                "folder": Option("folder", "/home/aces/pina-colada/packets/", "name of folder to save packets", True),
                }
        self.help_text = "Sniffs all packets and stores them in a directory."

    def listen(self):
        while True:
            try:
                pkts = sniff(timeout=float(self.get_value("rate")))
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                wrpcap(str(self.get_value("folder")) + str(st) + ".pcap", pkts)
            except Exception as e:
                print "failure"
                print e

    def restore(self):
        pass

    def launch(self):
        os.system("mkdir " + str(self.get_value("folder")))
        try:
            thread.start_new_thread (self.listen, ()) 
        except Exception as e:
            print "Thread creation failed"
            print e
