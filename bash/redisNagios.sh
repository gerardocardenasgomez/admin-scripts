#!/usr/bin/env bash
# Author: Gerardo Cardenas-Gomez
# Email: gerardo@gerardobsd.com
# Version: 0.0.1
# TODO This file currently connects to Redis too many times--fix this!
# TODO Consider breaking up this file into more than one script.

############

# This function is going to return values that are requested
# 
# TODO possibly figure out a way to do this without returning
#     having to connect to the database so many times.
# 
# Usage:
#     redis_fetch <ip_addr> <INFO|CONFIG> <parameter>
# 
# TODO get better at checking for mistakes and returning proper exit codes
# 
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


# This function will be used with Nagios. It checks the rdb_last_save_time
#     and then sees if it the last date was within a specified range.
# 
# Usage:
#     check_last_backup <ip_addr> <soft check> <hard check>
# 
# The soft check will produce a warning and exit code 1
# The hard check will produce a critical error and exit code 2

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

# This function checks the database for the back up file name and directory.
#     The check is done so that the script does not end up backing up a 
#     stale file that the DB is not actually using. Then, the function will copy
#     the back up to the specified target directory and then appending
#     a timestamp of YEAR, MONTH, DAY, HOUR to the file so it can
#     display properly with commans such as ls.
# 
# Usage:
#     perform_backup <ip_addr> <target directory

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
            now=$(date +%Y%m%d%H)
            echo "OK: Copied ${redis_dir}/${redis_dbname} to $target_dir/${redis_dbname}.${now}"
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
