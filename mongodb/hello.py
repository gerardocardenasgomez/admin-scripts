#!/usr/bin/env python
from bottle import route, run
import pymongo

@route('/')
def index():
    connection = pymongo.MongoClient('localhost', 27017)
    db = connection.test
    names = db.names

    results = names.find_one({ "name" : "Tom" })

    page_output = "Name: {0} Age: {1}".format(results["name"], results["age"])

    return page_output

run(host='localhost', port=8080, debug=True)
