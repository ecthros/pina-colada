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

import scans
import network
import traceback

from capabilities import *
from scapy import *
import network
from start import *
sys.path.append("capabilities")

class PinaColada(object):
    
    def __init__(self):
        self.default_iface = "en0" if (sys.platform == "darwin") else "eth0"
        self.localIP = self.get_local_ip(self.default_iface)
        self.network = network.init_network(self)
        self.cur = self.network.cur
        self.categories = None

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
                if file[-3:] == ".py" and file != "__init__.py":
                    bds.append(str(file).replace(".py", ""))
                    if echo:
                        print (len(path)*'  ') + "-", str(file).replace(".py", "")
        return bds
    
    def reload(self):
        pass

    def get_categories(self):
        return ["auxiliary", "dos", "arp", "enumeration", "sniff", "exploitation", "scan"]

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
            loc, bd =  bd.rsplit("/", 1)
            if "capabilities/" + loc not in sys.path: 
                sys.path.insert(0, "capabilities/" + loc)
            mod = importlib.import_module(bd)
            clsmembers = inspect.getmembers(sys.modules[bd], inspect.isclass)
            cap = [m for m in clsmembers if m[1].__module__ == bd][0][1](self) 
            return cap
        except Exception as e:
            print e
            traceback.print_exc()
            return None
