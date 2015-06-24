#!/usr/bin/env bash

redis_fetch () {
    ip_addr=$1
    query_type=$2
    target=$3

    case $query_type in
    *INFO*)
        results=$(redis-cli -h $ip_addr INFO | grep "$target:" | awk -F: '{print $2}' | tr -d '\r') 
        ;;
    *CONFIG*)
        results=$(redis-cli -h $ip_addr CONFIG GET $target | perl -ne 'print if $. == "2";')
        ;;
    esac

    echo $results
}

check_last_backup() {
    ip_addr=$1
    hours_soft=$2
    hours_hard=$3

    results=$(redis_fetch $ip_addr INFO rdb_last_save_time)
    now=$(date +%s | tr -d '\r')

    difference=$((now - results))
    hours=$((difference / 3600))

    if [[ $hours -gt $hours_soft ]]; then
        if [[ $hours -gt $hours_hard ]]; then
            echo "CRITICAL: It has been $hours hours since the last save!"
            exit 2
        fi
    
        echo "WARNING: It has been $hours hours since the last save!"
            exit 1
    else
        echo "OK: It has been $hours hours since the last save."
        exit 0
    fi
}

perform_backup() {
    ip_addr=$1
    target_dir=$2

    redis_dbname=$(redis_fetch $ip_addr CONFIG dbfilename)
    redis_dir=$(redis_fetch $ip_addr CONFIG dir)

    redis_output=$(redis-cli -h $ip_addr BGSAVE)
    if [[ ! $redis_output =~ .*started.* ]]; then
        echo $redis_output
        exit 99
    fi
    
    while :
    do
        result=$(redis_fetch $ip_addr INFO rdb_bgsave_in_progress)
        if [[ $result == "0" ]]; then
            echo "we're copying ${redis_dir}/${redis_dbname} to $target_dir"
            exit 0
        fi

        sleep 1
    done

    #echo $redis_dbname
    #echo $redis_dir
}

ip_addr=$1
action=$2
parameter=$3

case $action in
    FETCH|INFO)
        redis_fetch $ip_addr INFO $parameter
        ;;
    BACKUP)
        perform_backup $ip_addr $parameter
        ;;
    CONFIG)
        redis_fetch $ip_addr CONFIG $parameter
        ;;
    CHECK_BACKUP)
        check_last_backup $ip_addr $parameter $4
        ;;
esac
