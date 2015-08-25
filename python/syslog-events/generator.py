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

new_user_counter = 0

f = open('datafile', 'w')

while count < repeats:
    this_event = random.choice(events)
    this_result = random.choice(results)
    this_device = random.choice(results)

    syslog.openlog(this_event)

    message = uuid.uuid4().hex + " " + str(int(os.urandom(32).encode('hex'), 16)) + " " + this_event + " " + this_result + " " + this_device + "\n"

    count += 1

    if this_event == "new_user":
        new_user_counter += 1

    #print message
    sleep(0.0005)
    
    if (count % 1000) == 0:
        print count
    syslog.syslog(message)
    f.write(message)

print "Messages published: {0}, new_user published: {1}".format(count, new_user_counter)
f.close()
