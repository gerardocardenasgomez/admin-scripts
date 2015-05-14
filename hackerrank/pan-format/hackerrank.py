#!/usr/bin/env python
import re
import sys

def string_check(string_input):
    regex = r'hackerrank'
    result = re.search(regex, string_input, re.IGNORECASE)

    if result is not None:
        return True
    else:
        return False

string_array = []
counter = 1
input_count = 0
string_counter = 0

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

for item in string_array:
    if string_check(item):
        string_counter += 1

    if input_count > 0:
        input_count = input_count - 1
    if input_count == 0:
        break
print string_counter
