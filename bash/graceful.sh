#!/usr/bin/env bash

domain=$1

while true
do
    es_string=$(curl -s -XGET "http://$domain:9200/lists/_stats")
    echo $es_string
    es_cluster=$(curl -s -XGET "http://$domain:9200/_cluster/health")
    echo $es_cluster
    echo "-----------------"
    sleep 1
done
