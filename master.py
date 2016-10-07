from scans import *
import subprocess
from network import *
from scapy import *

if __name__ == "__main__":
    if os.getuid() != 0:
        print "Please run me as root!"
        sys.exit()
    print wifi_scan()
