#!/usr/bin/env python
import re
import commands

def compile_regex(reg_ex):
    return re.compile(reg_ex)

# reg_ex = '\d+\.\d+\.\d+\.\d+\:\d+'
ip_addr = compile_regex('\d+\.\d+\.\d+\.\d+\:\d+')

# reg_ex = '\d+\.\d+\.\d+\.\d+\:\d+\s+\d+\.\d+\.\d+\.\d+'
port_relations = compile_regex('\d+\.\d+\.\d+\.\d+\:\d+\s+\d+\.\d+\.\d+\.\d+\:\d+')

# port_regex = ':(\d+)'
port_number = compile_regex(':(\d+)')

server_to = set()
client_to = set()
listening_set = set()
port_relationships_set = set()

def print_set(set_input, title):
    print " - - - - {0} - - - - ".format(title)

    if set_input:
        sorted_set_input = sorted(set_input)
        for item in sorted_set_input:
            print "|    {0}".format(item)
    else:
        print "|    None"

    print " - - - - - - - -"
    print '\n'

def add_port_relations(ip_string):
    ip_array = ip_string.split(':')

    local_ip = ip_array[0]
    local_port = ip_array[1]

    local_port = int(ip_array[1].split(" ")[0])

    remote_ip = ip_array[1].split(" ")[-1]

    remote_port = int(ip_array[2])

    if local_port < 12000 and remote_port > 12000:
        string_length = len(local_ip) + len(str(local_port)) + 1
        num_of_spaces = 37 - string_length
        parsed_string = local_ip + ':' + str(local_port) + (' ' * num_of_spaces) + remote_ip
    elif local_port > 12000 and remote_port < 12000:
        string_length = len(local_ip)
        num_of_spaces = 37 - string_length
        parsed_string = local_ip + (' ' * num_of_spaces) + remote_ip + ':' + str(remote_port)
    else:
        parsed_string = ip_string

    port_relationships_set.add(parsed_string)

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

    match = re.findall(port_relations, line)
    if match:
        if '0.0.0.0' in match[0]:
            continue
        add_port_relations(match[0])        

print_set(server_to, "Server to")
print_set(client_to, "Client to")
print_set(listening_set, "Listening Interfaces")
print_set(port_relationships_set, "Port Relationships")
