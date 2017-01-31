#!/usr/bin/env python
from __future__ import print_function
import logging
# This supresses an error about not having IPv6 routing
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import sys
from StringIO import StringIO
import time
from scapy.all import *
import datetime

def ping_ip(ip, port, count):
    total = 0

    for i in range(count):
        start = time.time() * 1000

        packets = 0
        lost = 0

        # TODO how does this work exactly?
        ans,unans = sr( IP(dst=ip)/TCP(dport=port,flags="S"), inter=0.5,retry=-2,timeout=1, verbose=0)

        end = time.time() * 1000


        # ans.summary is going to print stuff to stdout so stdout needs to be captured here
        capture = StringIO()
        save_stdout = sys.stdout
        sys.stdout = capture

        # Lambda to iterate over the data from sr()
        ans.summary( lambda(s,r) : r.sprintf("%IP.dst% > %IP.src%") )

        sys.stdout = save_stdout

        # Print line here if you want to show what output came from the lambda
        for line in capture.getvalue():
            if line is not "":
                packets += 1
            else:
                lost += 1

        total_time = (end - start)

        print(datetime.datetime.now(), end="")
        print(" Time: {0:10.0f} ms".format(total_time), end="")
        print(" Packets: {0}".format(packets))

        if (lost > 0):
            print(" Lost: {0}".format(lost), end="")
