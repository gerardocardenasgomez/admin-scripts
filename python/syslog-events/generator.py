#!/usr/bin/env python
import uuid
import syslog
import os
import random
import sys
from time import sleep

repeats = int(sys.argv[1])
count = 0

events = [ "new_points", "new_user", "new_session", "get_reward" ]
results = [ "successful", "failure", "else" ]
devices = [ "android", "windows", "iphone", "blackberry" ]

f = open('datafile', 'w')

while count < repeats:
    this_event = random.choice(events)
    this_result = random.choice(results)
    this_device = random.choice(results)

    message = uuid.uuid4().hex + " " + str(int(os.urandom(32).encode('hex'), 16)) + " " + this_event + " " + this_result + " " + this_device + "\n"

    count += 1

    #print message
    sleep(0.0005)
    
    if (count % 1000) == 0:
        print count
    syslog.syslog(message)
    f.write(message)

print "Messages published: {0}".format(count)
f.close()
