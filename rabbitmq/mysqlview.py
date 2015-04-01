#!/usr/bin/env python

import MySQLdb

def mysql_view(host, username, password, db_name, query):
    mydb = MySQLdb.connect(host=host,user=username,passwd=password,db=db_name)
    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM sanitizedthis.users WHERE username LIKE %s", (query,))
    results = cursor.fetchall()

    print results

    mydb.commit()
    mydb.close()

if __name__ == "__main__":

    host = "localhost"
    username = "sanitizedthis"
    password = "sanitizedthis"

    db_name = "sanitizedthis"

    query = "sanitizedthis"

    mysql_view(host, username, password, db_name, query)
