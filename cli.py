import os
import cmd
import sys
import traceback
import netifaces as ni
import core
from sniff import *
from network import *

from colorama import *
from Tkinter import *
from capabilities import *

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET


class PinaColadaCLI(cmd.Cmd):
    prompt = Fore.BLUE + ">> " + Fore.RESET
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.core = core.PinaColada()
        self.ctrlc = False
        self.ascii_art()
        print "Welcome to Pina Colada, a powerful Wifi Pineapple. Type \"help\" to see the list of available commands."
        print "Packets are being stored in the packets directory."
   
    def ascii_art(self):
        print "    ____  _  /\//          ______      __          __        ' ."    
        print "   / __ \(_)//\/ ____ _   / ____/___  / /___ _____/ /___ _   \~~~/"
        print "  / /_/ / / __ \/ __ `/  / /   / __ \/ / __ `/ __  / __ `/    \_/"
        print " / ____/ / / / / /_/ /  / /___/ /_/ / / /_/ / /_/ / /_/ /      Y"
        print "/_/   /_/_/ /_/\__,_/   \____/\____/_/\__,_/\__,_/\__,_/      _|_"

    def print_help(self, lst):
        it = iter(lst)
        for x in it:
            print("{0:<20} {1:<25}".format(x, next(it)))
    
    def do_help(self, args):
        print "\nAvailable commands are: "
        print "======================="
        self.print_help(["list", "lists currently loaded targets, available capabilities, and enabled modules.", "quit", "quits","use <capability>", "engages a capability for use. Run \"list\" or \"list capabilities\" for a full list of capabilities.", "network", "shows all computers on the network"])
    
    def do_quit(self, args):
        self.quit()

    def do_clear(self, args):
        os.system("clear")
        
    def do_use(self, args):
        cap = self.core.instantiate(args)
        if cap is None:
            print(BAD + "An unexpected error occured.")
            return
        cli = CapabilityInterface(self, cap).cmdloop()

    def do_network(self, args):
        self.core.network.cur.execute("Select * from computers")
        print "ID\tIP\t\tMAC\t\t\tPorts\tLast Date"
        for computer in self.core.network.cur.fetchall():
            print str(computer[0]) + "\t" + str(computer[1]) + "\t" + str(computer[2]) + "\t" + str(computer[3]) + "\t" + str(computer[4])
            

    def complete_use(self, text, line, begin_index, end_index):
        line = line.rsplit(" ")[1]
        segment = line.split("/")
        if len(segment) == 1:
            categories = self.core.get_categories()
            opts = [item+"/" for item in categories if item.startswith(text)]
            if opts == []:
                return [category+"/"+item for category in categories for item in self.core.get_capabilities(category) if item.startswith(text)]
            return opts
        if len(segment) == 2:
            bds = self.core.get_capabilities(segment[0]) 
            return [item for item in bds if item.startswith(text)]

    def do_list(self, args):
        if args == "capabilities" or len(args) == 0:
            print(GOOD+ "Available capabilities: ")
            for cat in self.core.get_categories():
                caps = self.core.get_capabilities(cat)
                if caps != []:
                    print(" " + INFO + cat)
                for cap in caps:
                    print("   - " + cap)
        
        if len(args) != 0 and args != "targets" and args != "capabilities" and args != "modules":
            print(BAD + "Unknown option " + args)

    def preloop(self):
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}
    def do_history(self, args):
        print self._hist
    def do_exit(self, args):
        self.quit()
    def precmd(self, line):
        self._hist += [ line.strip() ]
        self.ctrlc = False
        return line
        
    def default(self, line):       
        try:
            print GOOD + "Executing \"" + line + "\""
            os.system(line)
        except Exception, e:
            print e.__class__, ":", e 
    
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            if not self.ctrlc: 
                self.ctrlc = True
                print("\n" + BAD + "Please run \"quit\" or \"exit\" to exit, or press Ctrl-C again.")
                self.cmdloop()
            else:
                print("")
                self.quit()            
    
    def do_EOF(self, line):
        quit()
        return
    
    def emptyline(self):
        return
    
    def quit(self):
        print(BAD + "Exiting...")
        self.network.cur.close()
        exit()
        return

def main():
    PinaColadaCLI().cmdloop()


if __name__ == "__main__":
    if os.getuid() != 0:
        print BAD + "Please run me as root!"
        sys.exit()
    main()


#    start_sniffing()
    #init_scan()
   # time.sleep(3600)
