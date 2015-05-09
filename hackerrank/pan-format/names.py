#!/usr/bin/env python
import re
import sys

input_array = []
counter = 1

while 1:
    try:
        line = sys.stdin.readline()
        line = line.rstrip('\n')
        input_array.append(line)
    except KeyboardInterrupt:
        break

    if not line:
        break


first_name = input_array[0]
last_name = input_array[1]

print "Hello {0} {1}! You just delved into python.".format(first_name, last_name)
