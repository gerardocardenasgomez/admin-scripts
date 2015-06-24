#!/usr/bin/env bash
#ip_addr=$1
target=$1

ip_addr='10.240.30.144'

results=$(redis-cli -h $ip_addr INFO | grep "$target:" | awk -F: '{print $2}' | tr -d '\r')

echo $results
