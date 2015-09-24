#!/usr/bin/env python
import sys
import os
import os.path
import re

# Dictionary with IP addresses as Keys and their counter as values
# 
ip_db = {}
#

# ip_addr matches valid IP addresses
# full_uri matches something such as /wp-content/uploads/2015/06/file.png
# domain uri matches my.example.com
# document_uri matches /wp-file.php
#
ip_addr_pattern = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
full_date_pattern = r'\d+\/\w+\/\d+(:\d+){1,}'
full_uri_pattern  = r'(\w+\.)?([A-z0-9-_]+\/){1,}[A-z0-9-_]+\.?[A-z]+'
domain_uri_pattern = r'([A-z0-9-_]+)?\.?[A-z0-9-_]+\.(com)'
document_uri_pattern = r'\/[A-z0-9-_]+\.(php|com|css|js)'
# Compile patterns for efficiency
ip_addr = re.compile(ip_addr_pattern)
full_date = re.compile(full_date_pattern)
full_uri = re.compile(full_uri_pattern)
domain_uri = re.compile(domain_uri_pattern)
document_uri = re.compile(document_uri_pattern)
#
#

# parse_line accepts a string with a log event
# parse_line should return at least an IP address
# Ideally it should return IP address + resource 
#
def parse_line(line):
    result = ''
    
    split_line = line.split(' ')
    for string in split_line:
        if (re.match(ip_addr, string)):
            result += string + ' '
            if string in ip_db:
                ip_db[string] = ip_db[string] + 1
            else:
                ip_db[string] = 1
        elif (re.search(full_date, string)):
            string = string.replace('[', '')
            result += string + ' '
        elif (re.search(full_uri, string)):
            result += string + ' '
        elif (re.search(domain_uri, string)):
            result += string + ' '
        elif (re.search(document_uri, string)):
            result += string + ' '
        else:
            continue

    if result == '':
        return None
    else:
        return result

# Check that the arguments are all proper files and are accessible
# os.access() would be enough except that directories will also return true for os.access()
#
for arg in sys.argv[1:]:
    if os.path.isfile(arg) and os.access(arg, os.R_OK):
        continue
    else:
        print "File does not exist or unable to read: {0}".format(arg)
        exit(1)

# For each file, parse through every line
#
for arg in sys.argv[1:]:
    file = open(arg)
    
    while True:
        lines = file.readlines(1000000)
        if not lines:
            break
        for line in lines:
            parsed_string = parse_line(line)
            if parsed_string is not None:
                print arg + ' % ' + parsed_string

# Make it easy to find the results portion by grepping for '--'
# Make it visually clear that the following text is for results
#
print '-- + --' * 10

# Print out the number of times each IP address was found in the file(s)
# Items that appear only once are probably okay -- ignore those
#
for key,value in ip_db.items():
    if value > 1:
        print "{0} -- {1}".format(value, key)
