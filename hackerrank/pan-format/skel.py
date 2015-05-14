#!/usr/bin/env python
import re
import sys

def custom_function(pan_number):
    pass

input_array = []
counter = 1
input_count = 0

while 1:
    try:
        line = sys.stdin.readline()

        if counter == 1:
            counter = 0
            input_count = int(line)
            continue

        line = line.rstrip('\n')
        input_array.append(line)
    except KeyboardInterrupt:
        break

    if not line:
        break

for item in input_array:
    if custom_function(item):
        pass

    if input_count > 0:
        input_count = input_count - 1
    if input_count == 0:
        break

