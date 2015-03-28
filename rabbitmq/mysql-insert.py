#!/usr/bin/env python
import datetime
import MySQLdb

today = datetime.date.today()

host = "localhost"
username = "user"
password = "pass"

db_name = "db"

script_id = 2
user_id = 1
dbDate = "{0}-{1:02d}-{2}".format(today.year,today.month,today.day)
completed = 0

mydb = MySQLdb.connect(host=host,user=username,passwd=password,db=db_name)
cursor = mydb.cursor()

tuple = (script_id, user_id, dbDate, completed)

cursor.execute("INSERT INTO pyrabbit.requests (script_id,user_id,date,completed) VALUES (%s,%s,%s,%s);", tuple)

mydb.commit()
mydb.close()
