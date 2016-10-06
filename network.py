from scapy.all import *
import logging
from scans import *
import subprocess
import re
import psycopg2

#All other computers should be in an array of type computer, having (so far) an ip and a MAC address.
class Computer(object):
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac


#The overall object, called master, creates its own ip, subnet, and list of other computers on the network.
#Fields:
#   ip -> the ip of this computer
#   subnet -> the subnet (takes the ip, sticks a 0 and /24 at the end
#   otherComps -> a result of running arping against the network (gives back unparsed packets)
#   comps -> A list of the computers on the network
class Network(object):
    def findIP(self):
        proc = subprocess.Popen(["ifconfig | grep inet | head -n1 | cut -d\  -f12 | cut -d: -f2"], stdout=subprocess.PIPE, shell=True)
        self.ip = proc.stdout.read()[:-1]
    def findSubnet(self):
        self.subnet = re.search("(\d*\.\d*\.\d*\.)", self.ip).group(0) + "0/24"
    def arpAll(self):
        self.otherComps = arping(self.subnet, verbose=0)
    def profile(self):
        self.comps = []
        x,y = self.otherComps
        for item in x:
            a,b = item
            self.comps.append(Computer(a.pdst, b.src))
    def connect(self):
        self.conn = psycopg2.connect("dbname='network' user='aces' host='localhost' password='aces'")
        self.cur = self.conn.cursor()

    def __init__(self):
        self.findIP()
        self.findSubnet()
        self.arpAll()
        self.profile()
        self.connect()

def init_scan():
    thisComp = Network()
    for comp in thisComp.comps:
        thisComp.cur.execute("INSERT INTO computers(ip,mac,ports) VALUES (%s, %s, %s)", (comp.ip, comp.mac, syn_scan(comp.ip, (0,1000))))

    thisComp.conn.commit()
    thisComp.cur.close()
