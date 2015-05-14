#!/usr/bin/env python
import re
import sys
import collections

def get_number(regex, number):
    result = re.search(regex, number)
    if not result:
        print number
        print "none found"
    return result.group()

def add_number(number, number_array):
    CountryCode_regex   = r'^\d{1,3}'
    LocalAreaCode_regex = r'(?<=[ -.])\d{1,3}(?=[ -.])'
    Number_regex        = r'(?<=[ -.])\d{4,10}\b'

    CountryCode     = get_number(CountryCode_regex, number)
    LocalAreaCode   = get_number(LocalAreaCode_regex, number)
    Number          = get_number(Number_regex, number)

    new_num = Phone(CountryCode=CountryCode, LocalAreaCode=LocalAreaCode, Number=Number)

    number_array.append(new_num)


string_array = []
counter =  1
input_count = 0
number_array = []

Phone = collections.namedtuple('Phone', ['CountryCode', 'LocalAreaCode', 'Number'])

while 1 :
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


for number in string_array:
    if number == '':
        break
    add_number(number, number_array)

for number in number_array:
    print"CountryCode={0},LocalAreaCode={1},Number={2}".format(number.CountryCode, number.LocalAreaCode, number.Number)
