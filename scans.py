from scapy.all import *

#This scans the host on all ports in the array named ports
#This function uses a syn scan. This function is also much slower :(

def slow_syn_scan(host, ports):
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    packetlist = []
    for dstPort in ports:
        srcPort = random.randint(1025,65534)
        resp = sr1(IP(dst=host)/TCP(sport=srcPort,dport=dstPort,flags="S"),timeout=1,verbose=0)
        if (str(type(resp)) == "<type 'NoneType'>"):
            print host + ":" + str(dstPort) + " is filtered (silently dropped)."
        elif(resp.haslayer(TCP)):
                if(resp.getlayer(TCP).flags == 0x12):
                    send_rst = sr(IP(dst=host)/TCP(sport=srcPort,dport=dstPort,flags="R"),timeout=1,verbose=0)
                    print host + ":" + str(dstPort) + " is open."
                #elif (resp.getlayer(TCP).flags == 0x14):
                    #print host + ":" + str(dstPort) + " is closed."
        elif(resp.haslayer(ICMP)):
            if(int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                print host + ":" + str(dstPort) + " is filtered (silently dropped) but host is up."


#This is a fast syn scan.
def syn_scan(target, ports):
    print "Beginning Scan...\n"
    ans,unans = sr(IP(dst=target)/TCP(dport=ports),timeout=.1,verbose=0)
    rep = []
    for s,r in ans:
        if not r.haslayer(ICMP):
            if r.payload.flags == 0x12:
                rep.append(r.sprintf("%sport%"))
    return rep

#TESTING - syn scans first 500 ports (slow)
#syn_scan("10.0.0.35", range(1,500))

#print fast_scan("10.0.0.35", (0,10000))
