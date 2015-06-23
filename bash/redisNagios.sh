#!/usr/bin/env bash

hours_hard=12
hours_soft=6

redis_server=$1

results=$(redis-cli -h 127.0.0.1 INFO Persistence | grep rdb_last_save_time | awk -F: '{print $2}' | tr -d '\r')
now=$(date +%s | tr -d '\r')

#echo $results
#echo $now

difference=$((now - results))
hours=$((difference / 3600))

if [[ $hours -gt $hours_soft ]]; then
    if [[ $hours -gt $hours_hard ]]; then
        echo "CRITICAL: It has been $hours since the last save!"
        exit 2
    fi
    
    echo "WARNING: It has been $hours since the last save!"
else
    echo "OK: It has been $hours since the last save."
fi
