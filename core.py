import sys
import os
import logging
import netifaces as ni
import importlib
import inspect
import socket

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import scans
import network
import traceback

from capabilities import *
from scapy import *
from sniff import *
from network import *
sys.path.append("capabilities")

class PinaColada(object):
    
    def __init__(self):
        self.localIP = self.get_local_ip()
        start_sniffing()
        self.network = init_network()
        self.cur = self.network.cur
        self.categories = None

    def get_local_ip(self):
        pass

    def walk(self,folder,echo=False):
        bds = []
        if echo:
            print(" " + INFO + folder.replace("capabilities/", ""))
        for root, dirs, files in os.walk(folder):
            del dirs[:] # walk down only one level
            path = root.split('/')
            for file in files:
                if file[-3:] == ".py":
                    bds.append(str(file).replace(".py", ""))
                    if echo:
                        print (len(path)*'  ') + "-", str(file).replace(".py", "")
        return bds
    
    def reload(self):
        pass

    def get_categories(self):
        return ["auxiliary", "dos", "arp", "enumeration", "exploitation"]

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
