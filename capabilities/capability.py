import os
import sys

from option import *
from colorama import *

class Capability(object):
    def __init__(self, core):
        self.options = {}
        self.core = core
        self.help_text = None
    
    def set_option(self, option, value):
        if option in self.options.keys():
            self.options[option].value = value
            return True
        else:
            return False

    def launch(self):
        return False
    
    def restore(self):
        return False

    def exec_command(self, comm):
        self.core.cur.execute(comm)
        return self.core.cur.fetchall()[0][0]

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None
    
    def get_options(self):
        return options
    
    def set_target(target):
        self.options['target'] = target


