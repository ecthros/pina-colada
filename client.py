import socket
import threading
import sys
import traceback
import os
import base64
import random
import ctypes
import importlib
import inspect
import zlib
import json
import time

from Crypto.Cipher import AES
from Crypto import Random
from datetime import datetime

VERBOSE = "-v" in sys.argv

DEBUG = "-d" in sys.argv

my_hwnd = 0
my_pid = os.getpid()
my_name = ""

SERVER_PORT = 9999
SERVER_IPS = ["127.0.0.1"]

VERSION = 0.59
ERR_MSG = "[!] Lost server connection. Please try again later."
SEP = "|:|"
END_SEP = "!:!"

if DEBUG:
    VERBOSE = True
    SERVER_PORT = 8888
    SERVER_IPS = ["127.0.0.1"]

####################################################################
#
# Message Types
#
####################################################################

MSG = 0
NEWC = 1
CLOSE = 2
INFO = 3
REQ = 4

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]
replace_seps = lambda m: m.replace("|::|", SEP).replace("!::!", END_SEP)
save_seps = lambda m: m.replace(SEP, "|::|").replace(END_SEP, "!::!")

def get_date():
    return "%02d:%02d:%02d" % (datetime.now().hour, datetime.now().minute, datetime.now().second)

class Client(object):
    def __init__(self, name, target_port, server_ips):
        self.port = target_port
        self.server_iter = iter(server_ips)
        self.server_ips = server_ips
        self.ip = self.server_iter.next()
        self.name = name
        self.socket = None

        self.VERBOSE = VERBOSE

        self.keys = {}
        self.message_history = {}
        self.prompt = ">> "

    def connect(self):
        client = None
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.ip, self.port))
                self.socket = client

                shared_prime, shared_base = client.recv(1024).split("|")
                shared_prime = int(shared_prime)
                shared_base = int(shared_base)
                client_secret = random.randint(0, 99)
                a = long(client.recv(1024))
                b = (shared_base**client_secret) % shared_prime
                client.send("%ld" % b)
                self.keys[client] = pad("%ld" % ((a ** client_secret) % shared_prime))

                conn = threading.Thread(target=self.receive, args=(client,))
                conn.start()

                self.send(NEWC, my_name)
                print("[*] Successfully connected.")

                client.settimeout(None)  # Remove the timeout
                self.client_input() # TODO
            except socket.timeout:
                if not self.set_backup():
                    client.close()
                    return False
                continue
            except EnvironmentError as e:
                if e.errno == 10061 and not self.set_backup():
                    client.close()
                    return False
                continue
            except Exception as e:
                print_exc(e, ERR_MSG, always=True)
                raw_input("")
                continue

    def client_input(self):
        self.server_down = False
        try:
            while not self.server_down:
                print("\r%s" % self.prompt),
                data = raw_input("")
                if not data: # TODO
                    continue
                self.send(MSG, data)
        except Exception as e:
            print e
        finally:
            self.socket.close()

    ####################################################################
    #
    # Message Handling
    #
    ####################################################################

    def send(self, message_type, data):
        print("<OUT: %s>" % self.pack_data(message_type, my_name, data))
        self.socket.send(self.encrypt(self.pack_data(message_type, my_name, data), self.socket))

    def encrypt(self, string, sock):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.keys[sock], AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(pad(zlib.compress(string))))

    def decrypt(self, msg, sock):
        enc = base64.b64decode(msg)
        cipher = AES.new(self.keys[sock], AES.MODE_CBC, enc[:16])
        return zlib.decompress(unpad(cipher.decrypt(enc[16:])))

    def unpack_data(self, msg):
        msgs = [replace_seps(s) for s in msg.split(SEP)]
        try:
            msgs[0] = int(msgs[0])  # convert type to int
        finally:
            return msgs

    def pack_data(self, message_type, name, data):
        return str(message_type) + SEP + save_seps(name) + SEP + save_seps(data) + END_SEP

    def print_msg(self, message):
        newline = message.find('\n')
        prompt = self.prompt
        msg_width = 80 - len(self.name) - 2 - 8  # 80 is max, 2 for ": ", 8 for date
        if newline != -1:  # has newline
            if newline < msg_width:
                print("\r" + "{:71} {:>8}".format(message[:newline], get_date())),
                print("\r" + message[newline+1:] + "\n" + prompt + self.current_buffer),
        elif len(message) > msg_width:
            rspace = message.rfind(" ", 0, 71)  # find the rightmost space
            if rspace > 20:
                print("\r" + "{:71} {:>8}".format(message[:rspace], get_date())),
                print("\r" + " " * (len(self.name)+2) + message[rspace+1:] + "\n" + prompt + self.current_buffer),
            else:  # one looooong word
                print("\r" + "{:71} {:>8}".format(message[:71], get_date())),
                print("\r" + " " * (len(self.name)+2) + message[71:] + "\n" + prompt + self.current_buffer),
        else:  # Will fit in one line
            print("\r" + "{:71} {:>8}".format(message, get_date()) + prompt + self.current_buffer),

    def handle_commands(self, command):
        full_command = command
        typ = REQ
        if len(command.split()) > 1:
            command = command.split()[0]
        if command in self.commands:
            typ = self.commands[command]
        elif command == "\\cls" or command == "\\clear":
            os.system("cls")
            return False
        elif command == "\\reload":
            self.check_version(self.json_obj, override=True) #TODO
            return False
        else:
            typ = REQ
        self.send(typ, full_command)

    def handle(self, sock, data):
        if VERBOSE:
            print("<IN: %s>" % data)

        message_type, name, data = self.unpack_data(data)
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
                    self.handle(sock, m)
        except Exception as e:
            sock.close()
        finally:
            sock.close()
            sys.exit()

if __name__ == "__main__":
    c = Client("Client", SERVER_PORT, SERVER_IPS).connect()
