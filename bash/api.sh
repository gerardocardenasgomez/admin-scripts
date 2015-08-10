#!/usr/bin/env bash
. aws_api.txt

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

if [[ $url = "" ]]; then
    echo "no url defined"
fi

echo \{\"host\":\"$HOSTNAME\",\"date\":\"$today\",\"time\":\"$time\",\"event\":\"$event\"\} > $temp_file

curl -XPOST $url -H "x-api-key: $api_key" -H "Content-Type: application/json" --data-binary @$temp_file

rm $temp_file
