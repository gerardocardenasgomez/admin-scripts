#!/usr/bin/env python
import pymongo
import datetime
from pymongo import MongoClient


# connect to database
connection = MongoClient('localhost', 27017)

db = connection.test

# handle to names collection
pydata = db.data

try:
    commit_data = pydata.find_one({"name": "user"})
    if not commit_data:
        raise exception
except:
    print "had to add data!"
    pydata.insert({"name": "user", "commitMessage": "Add variables to the file db.py", "createdAt": datetime.datetime.utcnow()})
    commit_data = pydata.find_one({"name": "user"})

print commit_data["name"]
print commit_data["commitMessage"]
