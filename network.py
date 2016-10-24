from scapy.all import *
import logging
from scans import *
import subprocess
import re
import psycopg2
import time
import datetime
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
        proc = subprocess.Popen(["uname -a"], stdout=subprocess.PIPE, shell=True)
        self.uname = proc.stdout.read()[:-1]
        if("kali" in self.uname):
            p1 = subprocess.Popen(["ip a"], stdout=PIPE, shell=True)
            proc = subprocess.Popen(["grep inet | grep 24 | awk -F\" \" '{print $2}'"], stdin=p1.stdout, stdout=PIPE, shell=True)
            self.ip = proc.stdout.read()[:-4]
        else:
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

def begin_scan(thisComp, portLow, portHigh):
    for comp in thisComp.comps:
        ports = syn_scan(comp.ip, (portLow, portHigh))
        ports = ','.join(ports)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        thisComp.cur.execute(" \
                UPDATE computers SET ip='{0}', ports='{1}', last_online='{2}' WHERE mac='{3}'; \
                INSERT INTO computers(ip,mac,ports,last_online) SELECT '{4}', '{5}', '{6}', '{7}' \
                WHERE NOT EXISTS (SELECT 1 FROM computers WHERE mac='{8}')" \
                .format(comp.ip, ports, st, comp.mac, comp.ip, comp.mac, ports, st, comp.mac))
    for network in wifi_scan():
        thisComp.cur.execute(" \
                UPDATE networks SET last_online='{0}' WHERE name='{1}'; \
                INSERT INTO networks(name, status, last_online) SELECT '{2}', 'online', '{3}' WHERE NOT EXISTS (SELECT 1 FROM networks WHERE name='{4}')" \
                .format(st, network, network, st, network))
    thisComp.conn.commit()
    thisComp.cur.close()
    return thisComp

def init_network():
    print "Initializing Network DB..."
    thisComp = Network()
    
    try:
        thread.start_new_thread(begin_scan, (thisComp, 22, 22))
    except Exception as e:
        print "Thread creation failed :("
        print e
    

    return thisComp



