#!/usr/bin/env bash

if [[ -e "/root/sec/aws_api.txt" ]] ; then
    . /root/sec/aws_api.txt
else
    . ./aws_api.txt
fi

temp_file=$(mktemp)
today=$(date +%Y-%m-%d)
time=$(date +%H:%M:%S)

fixed_input=""

for word in $@; do
    result=$(echo $word | tr -d '"')
    fixed_input+=$result
    fixed_input+=" "
done

event=$fixed_input

#echo $event

if [[ "$url" = "" ]]; then
    echo "no url defined"
fi

echo \{\"host\":\"$HOSTNAME\",\"date\":\"$today\",\"time\":\"$time\",\"event\":\"$event\"\} > $temp_file

curl -XPOST $url -H "x-api-key: $api_key" -H "Content-Type: application/json" --data-binary @$temp_file

if [[ "$1" == "ALERT" ]]; then
    echo \{\"message\":\"$HOSTNAME\ $today\ $time\ $event\"\} > $temp_file
    curl -XPOST "api.hipchat.com/v2/room/sys_alerts/message?auth_token=$hipchat_key" -H "Content-Type: application/json" --data-binary @$temp_file
fi

rm $temp_file
