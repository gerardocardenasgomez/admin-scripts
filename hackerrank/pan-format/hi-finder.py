#!/usr/bin/env python
import re
import sys

def search_hi(id_num):
    regex = r'^hi\s[^d]'
    
    result = re.search(regex, id_num, flags=re.IGNORECASE)
    if result is None:
        return False
    elif result:
        return True

input_array = []
counter = 1
input_count = 0
answer_array = []

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
    if search_hi(item):
       answer_array.append(item)

    if input_count > 0:
        input_count = input_count - 1
    if input_count == 0:
        break

for item in answer_array:
    print item
