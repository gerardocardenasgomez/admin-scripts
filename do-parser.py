#!/usr/bin/python
import urllib
import urllib2
import json

def print_dict(dictionary):
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print_dict(value)
        elif isinstance(value, list):
            print "**********"
            for x in value:
                print x["name"], " : ", x["networks"]["v4"][0]["ip_address"], " : ", x["id"]
        else:
            print "{0} : {1}".format(key,value)

opener = urllib2.build_opener(urllib2.HTTPSHandler())

url = "https://api.digitalocean.com/v2/droplets"
# Make sure that the token is sanitized!
token = ""
header = {'Authorization': 'Bearer ' + token}

droplets = urllib2.Request(url, None, header)

raw_data = opener.open(droplets).read()

json_data = json.loads(raw_data)

print_dict(json_data)
