#!/usr/bin/env python
import ConfigParser
import os
import os.path

auth_token = None

conf_path = './test.conf'

if os.path.isfile(conf_path) and os.access(conf_path, os.R_OK):
    config = ConfigParser.RawConfigParser()
    config.read('test.conf')
    auth_token = config.get('auth', 'auth_token')
else:
    auth_token = None


print auth_token
