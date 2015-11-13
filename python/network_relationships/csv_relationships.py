#!/usr/bin/env python
import re
import commands

reg_ex = '\d+\.\d+\.\d+\.\d+\:\d+'
ip_addr = re.compile(reg_ex)

port_regex = ':(\d+)'
port_number = re.compile(port_regex)

server_to = set()
client_to = set()
listening_set = set()

def print_set(set_input, title):
    if set_input:
        for item in set_input:
            print item

def add_listener(ip):
    listening_set.add(ip)

def add_server_to(server, client):
    final_string = ""
    final_string += server.split(':')[0]
    final_string += ",SERVER_TO,"
    final_string += client.split(':')[0]
    server_to.add(final_string)
    
def add_client_to(server, client):
    final_string = ""
    final_string += server.split(':')[0]
    final_string += ",CLIENT_TO,"
    final_string += client.split(':')[0]
    client_to.add(final_string)

def add_connections(server, client):
    server_match = re.search(port_number, server)
    client_match = re.search(port_number, client)

    if server_match and client_match:
        server_port = server_match.group(1)
        client_port = client_match.group(1)

        if int(server_port) < 10000:
            add_server_to(server, client)
            add_listener(server)
        if int(client_port) < 10000:
            add_client_to(server, client)
    
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
#print_set(listening_set, "Listening Interfaces")
