#!/usr/bin/env bash

function exit_status {
    if [[ "$1" -eq 0 ]]; then
        echo "Update complete"
        exit 0
    else
        echo "Error encountered"
        exit 1
    fi
}

if [[ "$1" == "update" ]]; then

    # Download scripts and config files with -N option to overwrite files
    wget -N "https://raw.githubusercontent.com/gerardocardenasgomez/admin-scripts/master/bash/api.sh"
    chmod 700 api.sh
    wget -N "https://raw.githubusercontent.com/gerardocardenasgomez/admin-scripts/master/sec/yum.conf"
    chmod 700 yum.conf
    wget -N "https://raw.githubusercontent.com/gerardocardenasgomez/admin-scripts/master/sec/sec.conf"
    chmod 700 sec.conf

    screen -list | grep -q '\.sec'
    exit_code=$?

    if [[ "$exit_code" -eq 0 ]]; then
        # If screen session is running in the background, send it ctrl+C to kill SEC
        #   then type out sec command and send Enter keypress
        screen -S "sec" -X stuff $'\cc' && screen -r "sec" -p0 -X stuff 'sudo sec -conf sec.conf -input /var/log/secure' && screen -r "sec" -p0 -X eval "stuff \015"
        screen_exit_code=$?

        exit_status $screen_exit_code
    else
        # If screen session is not running, execute it in the background.
        screen -dmS sec bash -c 'sec -conf /root/sec/sec.conf -conf /root/sec/yum.conf -input /var/log/secure -input /var/log/yum.log'
        screen_exit_code=$?

        exit_status $screen_exit_code
    fi

fi
