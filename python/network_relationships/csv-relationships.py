#!/usr/bin/env python
import re
import commands
import socket

reg_ex = '\d+\.\d+\.\d+\.\d+\:\d+'
ip_addr = re.compile(reg_ex)

port_regex = ':(\d+)'
port_number = re.compile(port_regex)

server_to = set()
client_to = set()
listening_set = set()

def print_set(set_input, title):
    print "".format(title)

    if set_input:
        for item in set_input:
            print "|    {0}".format(item)
    else:
        print "|    None"

    print " - - - - - - - -"
    print '\n'

def add_listener(ip):
    listening_set.add(ip)

def add_server_to(ip):
    server_to.add(ip.split(':')[0])
    
def add_client_to(ip):
    client_to.add(ip.split(':')[0])

def add_connections(server, client):
    server_match = re.search(port_number, server)
    client_match = re.search(port_number, client)

    if server_match and client_match:
        server_port = server_match.group(1)
        client_port = client_match.group(1)

        if int(server_port) < 10000:
            add_server_to(client)
            add_listener(server)
        if int(client_port) < 10000:
            add_client_to(client)
    
output = commands.getstatusoutput('netstat -lnaut')

for line in output[1].splitlines():
    match = re.findall(ip_addr, line)
    if match:
        if len(match) is 2:
            add_connections(match[0], match[1])
        else:
            add_listener(match[0])

print_set(server_to, "Server to")
print_set(client_to, "Client to")
print_set(listening_set, "Listening Interfaces")
