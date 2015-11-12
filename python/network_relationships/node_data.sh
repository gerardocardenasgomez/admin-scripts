#!/usr/bin/env bash
results=$(ifconfig | perl -ne 'print if s/.*addr:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*/$1/')

for line in $results; do
    echo "$line $HOSTNAME"
done
