#!/usr/bin/env python
import collections
import json
import optparse
import sys
import urllib2
import ConfigParser
import os
import os.path
#
# Do not make changes below this line
#

user_command = sys.argv[1]

# ****
#
# Getting input from a file is slightly more difficult.
# This method should accept a filename and return a "formatted" array that
#   dashing will accept.
#
#   TODO: Add a way to check that the file exists and that it is readable
#
# ****

def read_file(from_file):
    lines = []
    formatted_array = []
    
    with open(from_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        words = line.split(" ")
        pretty_msg = ' '.join(map(str, words[1:]))
        formatted_array.append({"label" : "{0}".format(words[0]), "value" : "{0}".format(pretty_msg)})

    return formatted_array


# ****
#
# Send a json document to the URL
# The host variable is what will specify the host for the module in Dashing
# Iterate over the fields, sending a json request with each iteration.
# Each field has a field.name and a field.value
#
# Allow the widget_type to be specified if necessary--normally text is fine.
#
# ****

def send_json(url, auth_token, host, fields_array, widget_type="text"):

    if widget_type == "text":
        for field in fields_array:
            url = "{0}/widgets/{1}_{2}".format(url, host, field.name)
            data = json.dumps({"auth_token" : auth_token, "text" : field.value})
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)
    elif widget_type == "list":
        for field in fields_array:
            url = "{0}/widgets/{1}_{2}".format(url, host, field.name)
            data = json.dumps({"auth_token" : auth_token, "items" : field.value})
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)

# ****
#
# Check a value!
# Iterate over the fields, check that they are not set to the default value of None.
# Each field has a field.name and a field.value
#
# ****

def check_value(fields_array):
    for field in fields_array:
        if field.value is None:
            print "{0} is required".format(field.name)
            exit(1)

# ****
#
# Setting up all the variables in named tuples so they're easier to
#   send around and parse.
#
# ****

Field = collections.namedtuple("Field", ['name', 'value'])

parser = optparse.OptionParser()

parser.add_option("-s", "--status", action="store", dest="status", default=None)
parser.add_option("-f", "--failed_logins", action="store", dest="failed_logins", default=None)
parser.add_option("-a", "--aide_status", action="store", dest="aide_status", default=None)
parser.add_option("-l", "--last_login", action="store", dest="last_login", default=None)
parser.add_option("-t", "--login_type", action="store", dest="login_type", default=None)
parser.add_option("-u", "--user_name", action="store", dest="user_name", default=None)
parser.add_option("-i", "--from_ip", action="store", dest="from_ip", default=None)

parser.add_option("--text", action="store", dest="text", default=None)
parser.add_option("--label", action="store", dest="label", default=None)
parser.add_option("--label-type", action="store", dest="label_type", default=None)
parser.add_option("--url", action="store", dest="url", default="http://127.0.0.1:3030")
parser.add_option("--auth_token", action="store", dest="auth_token", default=None)
parser.add_option("--host", action="store", dest="host", default="localhost")
parser.add_option("--config", action="store", dest="conf_path", default="./dash_submit.conf")
parser.add_option("--from-file", action="store", dest="from_file", default=None)

options, args = parser.parse_args()

# Set the options with a host_ prefix

host_status = Field("status", options.status)
host_failed_logins = Field("failed_logins", options.failed_logins)
host_aide_status = Field("aide_status", options.aide_status)
host_last_login = Field("last_login", options.last_login)
host_login_type = Field("login_type", options.login_type)
host_user_name = Field("user_name", options.user_name)
host_from_ip = Field("from_ip", options.from_ip)

text        =   options.text
label       =   options.label
label_type  =   options.label_type
url         =   options.url
auth_token  =   options.auth_token
host        =   options.host
conf_path   =   options.conf_path
from_file   =   options.from_file

# ****
#
# Set the token -- either use the token from options, token from config file, or set to None
#
# conf_file should have the same name as the .py executable
# conf_file should have the following format:
# [<section name>]
# <key>=<value>
#
# ****

# Check if conf_path is a file and is readable
if os.path.isfile(conf_path) and os.access(conf_path, os.R_OK) and auth_token == None:
    config = ConfigParser.RawConfigParser()
    config.read(conf_path)
    
    if auth_token == None:
        auth_token = config.get('data', 'auth_token')
    if url == None:
        url = config.get('data', 'url')
else:
    auth_token = None

# ****
#
# check_value accepts an array of Named Tuples.
# It then iterates over the value of every named tuple to
#   check if the value is None. If None, exit with code 0 and print error message
#
# send_json accepts a url and an array of Named Tuples.
# send_json is in charge of sending the json document to the specified URL
#
# Here, we first see if the user wants to send a field aide, status, failed logins, last_login, log, or all.
#   Then we check if the required fields have been assigned a value.
#   It is not this script's job to check that the values are proper, only that they are present.
#
# ****

if user_command == "aide" or user_command == "all":
    fields_array = [host_aide_status]
    check_value(fields_array)

    send_json(url, auth_token, host, fields_array)

if user_command == "status" or user_command == "all":
    fields_array = [host_status]
    check_value(fields_array)

    send_json(url, auth_token, host, fields_array)

if user_command == "failed_logins" or user_command == "all":
    fields_array = [host_failed_logins]
    check_value(fields_array)

    send_json(url, auth_token, host, fields_array)

if user_command == "last_login" or user_command == "all":
    fields_array = [host_last_login]
    check_value(fields_array)

    send_json(url, auth_token, host, fields_array)

# ****
#
# Allow the input to come from a log file. If from_file is specified, get the lines from the file.
#   Then, put those lines into a List of {'label':'text', 'value:'text'} documents that Dashing will accept.
#   Specify the widget_type as "list."
#
# ****

if user_command == "log" and from_file:
    formatted_array = read_file(from_file)

    host_login_text = Field("login_text", formatted_array)
    fields_array = [host_login_text]

    send_json(url, auth_token, host, fields_array, widget_type="list") 

    exit(0)

if user_command == "log" or user_command == "all":
    fields_array = [host_login_type, host_user_name, host_from_ip]
    check_value(fields_array)

    msg = "{0} {1} {2}".format(host_login_type.value, host_user_name.value, host_from_ip.value)
    host_login_text = Field("login_text", msg)

    fields_array = [host_login_text]

    send_json(url, auth_token, host, fields_array)

# ****
#
# Allow for a custom specification. Custom with --label-type="list" will require a file because that's where it gets the data from.
# Custom with --label=type="text" only requires the --text="<text>" option for its data.
#
# TODO: Possibly change all fields to use custom now
#
# ****

if user_command == "custom":
    if label_type == "list" and from_file:
        formatted_array = read_file(from_file)
        
        host_custom_text = Field("{0}".format(label), formatted_array)
        fields_array = [host_custom_text]

        send_json(url, auth_token, host, fields_array, widget_type="list")
    if label_type == "text":
        host_custom_text = Field("{0}".format(label), text)
        fields_array = [host_custom_text]

        send_json(url, auth_token, host, fields_array, widget_type="text")
