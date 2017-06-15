#!/usr/bin/env python
import sys

def get_float(user_input):
    try:
        return float(user_input)
    except ValueError:
        print "Error! Use only numbers. :)"
        sys.exit(1)

tip = 0
total = 0

billAmount = raw_input("What is the bill amount? ")
tipRate = raw_input("What is the tip rate? ")

billAmount_num = get_float(billAmount)
tipRate_num = get_float(tipRate) * 0.01


tip = billAmount_num * tipRate_num

total = billAmount_num + tip

print "Tip: ${:1.2f}".format(tip)
print "Total: ${:1.2f}".format(total)
