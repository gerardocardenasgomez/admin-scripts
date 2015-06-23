#!/usr/bin/env python
import random
import urllib2
import json
import sys
import time

domain = sys.argv[1]
url = 'http://{0}:9200/lists/words/'.format(domain)
print url
sanity = 5

with open('wordlist', 'r') as f:
    for line in f:
        word = line.rstrip('\n')
        id_num = str(random.randrange(1, 1000000))
        url = url + id_num
        word_length = len(word)
        data = json.dumps({"word" : word, "word_length" : word_length})
        
        req = urllib2.Request(url, data, {'Content-Type' : 'application/json'})
        retval = urllib2.urlopen(req)
        response = retval.read()

        if sanity > 0:
            print response
            sanity -= 1
    
        time.sleep(0.3)
        
        retval.close()
