import os
import pexpect
from colorama import *
import re

prompt = Fore.BLUE + ">> " + Fore.RESET

def base_test():
    cli = pexpect.spawn("sudo python cli.py")
    cli.expect(re.escape(prompt))

