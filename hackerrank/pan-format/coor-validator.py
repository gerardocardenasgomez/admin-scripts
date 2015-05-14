#!/usr/bin/env python
import re
import sys

def valid_coordinate(coordinate):
    # This regex is meant to validate a latitute/longitude pair that has the following format:
    # (x, y)
    # where -90 <= x <= +90
    #       -180 <= y <= +180
    # The plus and minus signs are not required but they may be there
    # The coordinates can have decimals 
    #   but if there is a decimal, it must be followed by numbers, e.g., (70., 70) 
    # There should always be an open and closing parentheses, and a space after the comma.
    regex = r'\([+-]?([0-9](\.\d+\,|\,)|[1-8][0-9](\.\d+\,|\,)|90(\,|\.0+\,))\s[+-]?([0-9](\.\d+\)|\))|[1-9][0-9](\.\d+\)|\))|1[0-7][0-9](\.\d+\)|\))|180(\.0+\)|\)))'
    # Please note this is the worst regex I have ever written
    
    result = re.search(regex, coordinate)
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
    if valid_coordinate(item):
       answer_array.append("Valid")
    else:
        answer_array.append("Invalid") 

    if input_count > 0:
        input_count = input_count - 1
    if input_count == 0:
        break

for item in answer_array:
    print item
