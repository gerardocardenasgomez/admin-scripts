#!/usr/bin/env python
import argparse
import redis_ping
import tcp_ping

parser = argparse.ArgumentParser()

# TODO Add options for port numbers and counters
parser.add_argument('-r', '--redis_host', action='store', default='127.0.0.1', required=False)
parser.add_argument('-p', '--ping_host', action='store', default='127.0.0.1', required=False)
parser.add_argument('-a', '--all_tests',  action='store_true', default=False, required=False)

args = vars(parser.parse_args())

redis_host = args['redis_host']
ping_host = args['ping_host']
all_tests = args['all_tests']

# TODO Add options to select which test(s) to perform
if all_tests:
    tcp_ping.ping_ip(ping_host, 22, 4)

if all_tests:
    redis_ping.ping_redis(redis_host, 6379, 5)
