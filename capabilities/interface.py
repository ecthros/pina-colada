import cmd
import subprocess
import math
import shlex
import importlib
import inspect
import sys
import os

from option import *
from colorama import *

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET


class CapabilityInterface(cmd.Cmd):
    
    def __init__(self, core, capability):
        cmd.Cmd.__init__(self)
        self.capability = capability
        self.core = core
        self.help_text = None
        self.prompt = Fore.RED + "("+self.capability.name+") " + Fore.BLUE + ">> " + Fore.RESET

    def complete_set(self, text, line, begin_index, end_index):
        line = line.rsplit(" ")[1]
        return [item for item in (self.capability.options.keys()) if item.startswith(text)]
    
    def do_launch(self, args):
        print GOOD + "Launching %s..." % (self.capability.name)
        self.capability.launch()
        return False

    def do_restore(self, args):
        print GOOD + "Restoring target..."
        self.capability.restore()
        return False

    def do_show(self, args):
        if args == "options":
            self.do_help(args)
        elif args == "modules":
            self.mods()
        else:
            print BAD + "Unknown option %s", args
    
    def do_set(self, args):
        args = shlex.split(args)
        bad_opt = BAD + "Unknown option %s" % args[0]
        if len(args) == 2 and args[0] in self.capability.options:  # TODO technically redundant
            self.capability.set_option(args[0].lower(), args[1])
            print(GOOD + "%s => %s" % (args[0], args[1]))
        elif len(args) != 2:
            print(BAD + "Usage: \"set <OPTION> <VALUE>\"")
        else:
            print(bad_opt)

    def exec_command(self, comm):
        self.core.cur.execute(comm)
        return self.core.cur.fetchall()[0][0]

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None

    def check_by_name(self, name):
        for mod in self.modules:
            if name.lower() == mod.name.lower():
                return True
        return False

    def do_EOF(self, line):
        print ""
        return True

    def emptyline(self):
        return

    def precmd(self, line):
        self._hist += [ line.strip() ]
        return line

    def do_history(self, args):
        print self._hist

    def do_exit(self, args):
        return True

    def do_quit(self, args):
        return True

    def default(self, line):
        print "passing to core"
        self.core.onecmd(line)

    def print_help(self, options):
        if options == {}:
            return
        vals = [str(o.value) for o in options.values()]
        l = int(math.ceil(max(map(len, vals)) / 10.0)) * 10
        print(("{0:<15} {1:<%s} {2:<30}" % str(l)).format("Option","Value", "Description"))
        print "="*(l+45)
        for name, opt in options.iteritems():
            print(("{0:<15} {1:<%s} {2:<30}" % str(l)).format(opt.name, opt.value, opt.description))

    def do_help(self, args):
        if self.help_text != None and self.help_text != "":
            print self.help_text
        self.print_help(self.capability.options) 
    
    def preloop(self):
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}
