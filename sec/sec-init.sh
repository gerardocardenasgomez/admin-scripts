#!/usr/bin/env bash

wget "https://raw.githubusercontent.com/gerardocardenasgomez/admin-scripts/master/bash/api.sh"
chmod +x api.sh

wget "https://raw.githubusercontent.com/gerardocardenasgomez/admin-scripts/master/bash/aws_api.txt"

echo "Type in URL"
read url

sed -i s#url_here#$url#g aws_api.txt

echo "Type in API key"
read api

sed -i s/api_key_here/$api/g aws_api.txt

chmod 600 aws_api.txt

wget ""
chmod 700 sec.conf

wget ""
chmod 700 yum.conf

yum install sec screen

screen -dmS sec bash -c 'sec -conf /root/sec/sec.conf -conf /root/sec/yum.conf -input /var/log/secure -input /var/log/yum.log'