#!/usr/bin/env bash
# Written by gerardo@perk.com
# Version 1.3
# Now with cleanup function! :O

BASEDIR=$(dirname "$0")
cd $BASEDIR

# Pick up variables from root, or current directory
if [[ -r "/root/sec/aws_api.txt" ]] ; then
    . /root/sec/aws_api.txt
else
    . ./aws_api.txt
fi

# Set up variables
# Temporary directory needs to be cleaned up 
temp_file=$(mktemp)
today=$(date +%Y-%m-%d)
time=$(date +%H:%M:%S)

fixed_input=""

# This function will run upon exit
# Remove the temporary directory
function cleanup {
    rm $temp_file
}
trap cleanup EXIT

# Concatenate the args into one string
for word in $@; do
    result=$(echo $word | tr -d '"')
    fixed_input+=$result
    fixed_input+=" "
done

event=$fixed_input

# This is used for AWS so if there is no URL,
#   leave the script
if [[ -z "$url" ]]; then
    exit 1
fi

# This format is supported by the custom AWS API
echo \{\"host\":\"$HOSTNAME\",\"date\":\"$today\",\"time\":\"$time\",\"event\":\"$event\"\} > $temp_file

# Make the call to AWS
curl -XPOST "$url" -H "x-api-key: $api_key" -H "Content-Type: application/json" --data-binary @$temp_file

# This used to be a HipChat alert, now it's Slack
# Call this section of code only if the first arg is "ALERT"
#   e.g. ./api.sh 'ALERT' "My error message here"
#   However, the "ALERT" string needs to be completely by itself as the first arg
# If the Slack URL is empty, exit the script with an error
if [[ "$1" == "ALERT" ]]; then
    
    if [[ -z "$slack_url" ]]; then
        exit 2
    fi

    echo \{\"channel\":\"#perk-sys_alerts\",\"username\":\"sysBot\",\"text\":\"$HOSTNAME\ $today\ $time\ $event\"\} > $temp_file
    curl -XPOST "${slack_url}" -H "Content-Type: application/json" --data-binary @$temp_file
fi
