import socket
import threading
import sys
import os
import base64
import random
import json
import traceback
import core
import pexpect
import re

from colorama import *
from Crypto.Cipher import AES
from Crypto import Random
from datetime import datetime

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET
prompt = Fore.BLUE + ">> " + Fore.RESET

SERVER_PORT = 9999
SERVER_IP = "127.0.0.1"

ERR_MSG = BAD + "Lost server connection. Please try again later."
SEP = "|:|"
END_SEP = "!:!"

####################################################################
#
# Message Types
#
####################################################################

MSG = 0
GET = 1
CLOSE = 2
INFO = 3
REQ = 4

CLI_INIT = 10
CLI = 11
CLI_RESP = 12

BS = AES.block_size
print BS
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]

replace_seps = lambda m: m.replace("|::|", SEP).replace("!::!", END_SEP)
save_seps = lambda m: m.replace(SEP, "|::|").replace(END_SEP, "!::!")

def get_date():
    return "%02d:%02d:%02d" % (datetime.now().hour, datetime.now().minute, datetime.now().second)


class PinaColadaSocket(object):
    def __init__(self, name, target_port, server_ip):
        self.port = target_port
        self.ip = server_ip
        self.name = name
        self.socket = None
        self.keys = {}
        print "[*] Attempting to connect to server"

    def connect(self):
        client = None
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.ip, self.port))
            self.socket = client
            shared_prime, shared_base = client.recv(10).split("|")
            shared_prime = int(shared_prime)
            shared_base = int(shared_base)
            client_secret = random.randint(0, 99)
            a = long(client.recv(1024))
            b = (shared_base**client_secret) % shared_prime
            client.send("%ld" % b)
            self.keys[client] = pad("%ld" % ((a ** client_secret) % shared_prime))
            client.settimeout(None)  # Remove the timeout
            self.send(MSG, "Client1")
            print("[*] Successfully connected.")
            receive_loop = threading.Thread(target=self.receive, args=(client,))
            receive_loop.start()
            self.send(CLI_INIT, "cli init")
            while True:
                line = raw_input(">> ")
                self.send(CLI, line)

        except Exception as e:
            print e
            print traceback.print_exc()
            raw_input("")
        finally:
            self.shutdown()

    def shutdown(self):
        print GOOD + "Exiting..."

    ####################################################################
    #
    # Message Handling
    #
    ####################################################################

    def send(self, message_type, data):
        #print "SENDING: <%d, %s>" %(message_type, data)
        self.socket.send(self.encrypt(self.pack_data(message_type, self.name, data), self.socket))

    def encrypt(self, string, sock):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.keys[sock], AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(pad(string)))

    def decrypt(self, msg, sock):
        enc = base64.b64decode(msg)
        cipher = AES.new(self.keys[sock], AES.MODE_CBC, enc[:16])
        return unpad(cipher.decrypt(enc[16:]))

    def unpack_data(self, msg):
        msgs = [replace_seps(s) for s in msg.split(SEP)]
        try:
            msgs[0] = int(msgs[0])  # convert type to int
        finally:
            return msgs

    def pack_data(self, message_type, name, data):
        return str(message_type) + SEP + save_seps(name) + SEP + save_seps(data) + END_SEP

    def print_msg(self, message):
        print message

    def handle(self, data):
        message_type, name, data = self.unpack_data(data)
        message_type = int(message_type)
        if message_type == CLI_INIT:
            self.send(CLI_RESP, self.cli_init())
        if message_type == CLI:
            self.send(CLI_RESP, self.cli_communicate(data))
        self.print_msg(data)
    ####################################################################
    #
    # Receive Handling
    #
    ####################################################################

    def receive(self, sock):
        try:
            while True:
                data = sock.recv(1024)
                msgs = filter(None, self.decrypt(data, sock).split(END_SEP))
                for m in msgs:
                    self.handle(m)
        except Exception as e:
            print e
            traceback.print_exc()
            sock.close()
        finally:
            sock.close()
            self.shutdown()

if __name__ == "__main__":
    PinaColadaSocket("Client", SERVER_PORT, SERVER_IP).connect()
