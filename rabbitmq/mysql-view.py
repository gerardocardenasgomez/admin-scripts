#!/usr/bin/env python

import MySQLdb

host = "localhost"
username = "user"
password = "pass"
tb_name = "table"

db_name = "db"

mydb = MySQLdb.connect(host=host,user=username,passwd=password,db=db_name)
cursor = mydb.cursor()

tuple = (tb_name,)
cursor.execute("SELECT * FROM pyrabbit.users WHERE username LIKE %s;", tuple)
results = cursor.fetchall()

print results

mydb.commit()
mydb.close()
