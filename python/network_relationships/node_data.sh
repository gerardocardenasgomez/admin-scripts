#!/usr/bin/env bash
results=$(ifconfig | perl -ne 'print if s/.*addr:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*/$1/')

for line in $results; do
    if [[ "$line" != '127.0.0.1' ]]; then
        echo "NODE_DATA $line" 
    fi
done
