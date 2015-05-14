#!/usr/bin/env bash
# TODO: Break the different actions into their own functions
# TODO: Make the query function more not awful

action=$1
server='10.132.219.64'
port='9200'

server_addr="$server:$port"

# $1 will be the exit code
# $2 will be the string returned by elasticsearch
#
print_results () {
    exit_code=$1
    return_string=$2

    if [[ "$exit_code" -eq 0 ]]; then
        echo "$return_string"
    else
        echo "Error! Exit code: $exit_code"
    fi

}

#
# format is: ./es_data BACKUP /_snapshot/name data.txt
#

if [[ "$action" == "BACKUP" ]]; then
    url=$2
    file=$3

    es_string=$(curl -s -XPUT "$server_addr/$url" -d @"$file")
    exit_code=$?

    print_results "$exit_code" "$es_string"
fi

#
# format is: ./es_put.sh PUT /megacorp/employee 99 data.txt
#                        $1           $2        $3   $4
if [[ "$action" == "PUT" ]]; then
    if [[ $3 =~ ^-?[0-9]+$ ]]; then
        url=$2
        id=$3
        file=$4
    else
        url=$2
        file=$3
        id=''
    fi

    es_string=$(curl -s -XPUT "$server_addr/$url/$id" -d @"$file")
    exit_code=$?

    print_results "$exit_code" "$es_string"
fi

#
# format is: ./es_put.sh GET /megacorp/employee _search last_name:Smith
#                         $1          $2           $3         $4
if [[ "$action" == "GET" ]]; then
    url=$2
    query_type=$3
    query_string=$4
    get_request_string='?q='

    #
    # If $query_string is empty, allow for /megacorp/employee/_search type queries
    # Otherwise, append the ?q= string for GET method 
    #
    if [[ "$query_string" != "" ]]; then
        query_type="/$query_type$get_request_string"
    fi

    es_string=$(curl -s XGET "$server_addr/$url$query_type$query_string")
    exit_code=$?

    print_results "$exit_code" "$es_string"
fi
