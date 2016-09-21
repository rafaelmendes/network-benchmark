#!/usr/bin/env python
 
import sys
from scapy.all import srp, Ether, ARP
 
if len(sys.argv) != 2:
    print "Usage: python arp-scan.py 192.168.1.0/24"
    sys.exit(1)
 
alive,dead=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=sys.argv[1]), timeout=2, iface='eno1' ,verbose=0)
print "MAC - IP"
for i in range(0,len(alive)):
    	print alive[i][1].hwsrc + " - " + alive[i][1].psrc