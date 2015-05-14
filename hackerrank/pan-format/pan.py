#!/usr/bin/env python
import re
import sys

def pan_check(pan_number):
    regex = r'[A-Z]{5}\d{4}[A-Z]'
    result = re.search(regex, pan_number)

    if result is not None:
        return True
    else:
        return False

pan_array = []
counter = 1
input_count = 0

while 1:
    try:
        line = sys.stdin.readline()

        if counter == 1:
            counter = 0
            input_count = int(line)
            continue

        pan_array.append(line)
    except KeyboardInterrupt:
        break

    if not line:
        break

for pan in pan_array:
    if pan_check(pan):
        print "YES"
    else:
        print "NO"

    if input_count > 0:
        input_count = input_count - 1
    if input_count == 0:
        break

