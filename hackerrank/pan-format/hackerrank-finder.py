#!/usr/bin/env python
import re
import sys

def find_positions(regex, my_string):
    results         = []
    end_position    = len(my_string) - 10
    score           = 2

    for num in re.finditer(regex, my_string):
        results.append(num.start())

    if not results:
        return -1

    if (0 not in results) and (end_position not in results):
        return -1

    if (0 in results) and (end_position not in results):
        return 1

    if (0 not in results) and (end_position in results):
        return 2

    if (0 in results) and (end_position in results):
        return 0

string_array = []
counter = 1
input_count = 0
regex = 'hackerrank'

while 1:
    try:
        line = sys.stdin.readline()

        if counter == 1:
            counter = 0
            input_count = int(line)
            continue

        string_array.append(line)
    except KeyboardInterrupt:
        break

    if not line:
        break

for line in string_array:
    if line == '':
        break

    line = line.rstrip()
    print find_positions(regex, line)
