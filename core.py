import sys
import os
import logging
import netifaces as ni
import importlib
import inspect
import socket
import fcntl
import struct
import netaddr

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import network
import traceback

from pythonwifi.iwlibs import Wireless
from capabilities import *
from scapy.all import *
import network
sys.path.append("capabilities")

class PinaColada(object):
    
    def __init__(self):
        self.interfaces = self.get_available_interfaces()
        self.default_iface = self.interfaces[0]
        self.localIP = self.get_local_ip(self.default_iface)
        self.network = network.init_network(self)
        self.cur = self.network.cur
        self.categories = None
        self.loaded_capabilities = {}
        self.cnc = self.localIP  # TODO

    def get_available_interfaces(self):
        interfaces = ni.interfaces()
        available = []
        for iface in interfaces:
            if ni.AF_INET in ni.ifaddresses(iface) and "lo" not in iface:
                available.append(iface)
        return available

    def set_interface(self, iface):
        if iface in ni.interfaces() and ni.AF_INET in ni.ifaddresses(iface):
            self.default_iface = iface
            self.localIP = self.get_local_ip(self.default_iface)
            return True
        else:
            return None

    def get_local_ip(self, iface):
        addrs = ni.ifaddresses(iface)
        ipinfo = addrs[socket.AF_INET][0]
        return ipinfo['addr']


    def get_local_mac(self, iface):
        return ni.ifaddresses(iface)[ni.AF_LINK][0]['addr']

    def get_cidr(self, iface):
        addrs = ni.ifaddresses(iface)
        ipinfo = addrs[socket.AF_INET][0]
        address = ipinfo['addr']
        netmask = ipinfo['netmask']
        return netaddr.IPNetwork('%s/%s' % (address, netmask))

    def walk(self, folder, echo=False):
        bds = []
        if echo:
            print(" " + INFO + folder.replace("capabilities/", ""))
        for root, dirs, files in os.walk(folder):
            del dirs[:] # walk down only one level
            path = root.split('/')
            for file in files:
                if file[-3:] == ".py" and file != "__init__.py" and not file.startswith("util_"):
                    bds.append(str(file).replace(".py", ""))
                    if echo:
                        print (len(path)*'  ') + "-", str(file).replace(".py", "")
        return bds

    def reload(self):
        pass

    def promisc(self, enable=True):
        if enable:
            os.system("ifconfig %s promisc" % self.default_iface)
        else:
            os.system("ifconfig %s -promisc" % self.default_iface)

    def get_categories(self):
        return ["auxiliary", "dos", "arp", "enumeration", "sniff", "exploitation", "scan"]

    def beacon(self, pkt):
        ap_list = []
        if pkt.haslayer(Dot11):
            if pkt.type == 0 and pkt.subtype == 8:
                if pkt.addr2 not in ap_list:
                    ap_list.append(pkt.addr2)
                    print "AP MAC: %s with SSID: %s " % (pkt.addr2, pkt.info)

    def get_wifis(self):
        print GOOD + "Sniffing for Wifi Beacons, output for newly disovered ones are below. Hit Ctrl-C when done."
        sniff(iface=self.default_iface, prn=self.beacon)

    def get_capabilities(self, category=None):
        caps = []
        if category is None:
            for cat in self.get_categories():
                caps += self.walk("capabilities/"+cat)
            return caps
        else:
            return self.walk("capabilities/"+category)

    def instantiate(self, args):
        try:
            bd = args.split()[0]
            loc, bd = bd.rsplit("/", 1)
            if "capabilities/" + loc not in sys.path: 
                sys.path.insert(0, "capabilities/" + loc)
            if bd not in self.loaded_capabilities:
                mod = importlib.import_module(bd)
                clsmembers = inspect.getmembers(sys.modules[bd], inspect.isclass)
                cap = [m for m in clsmembers if m[1].__module__ == bd][0][1](self)
                self.loaded_capabilities[bd] = cap
                return cap
            else:
                return self.loaded_capabilities[bd]
        except Exception as e:
            #print e
            #traceback.print_exc()
            return None
