from scans import *
import subprocess
from network import *
from scapy import *
from packets/sniff import *
import time

if __name__ == "__main__":
    if os.getuid() != 0:
        print "Please run me as root!"
        sys.exit()
    start_sniffing()
    init_scan()
    time.sleep(3600)
