#!/usr/bin/env bash
# TODO: Break the different actions into their own functions
# TODO: Make the query function more not awful

action=$1
url=$2
id=$3
file=$4
server='localhost'
port='9200'

server_addr="$server:$port"

# $1 will be the exit code
# $2 will be the string returned by elasticsearch
#
print_results () {
    if [ $1 -eq 0 ]; then
        echo $2
    fi
}

if [ "$action" == "PUT" ]; then
    es_string=$(curl -s -XPUT "$server_addr/$url/$id" -d @"$file")
    exit_code=$?

    print_results $exit_code $es_string
fi

if [ "$action" == "GET" ]; then
    es_string=$(curl -s XGET "$server_addr/$url/_search?q=$id")
    exit_code=$?

    print_results $exit_code $es_string
fi
