#!/usr/bin/env bash

echo "--ifconfig info--"
ifconfig | egrep -o 'addr\:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | egrep -o '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
#echo "--Netstat info--"
#netstat -ptan | awk 'NR>2 {print $4" | "$5" | "$6" | "$7}' | sort | uniq -w 20
