#!/usr/bin/env python
import datetime
import MySQLdb


def db_insert(host, username, password, db_name, script_id, user_id, completed, db_date=None):
    mydb = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)
    cursor = mydb.cursor()

    if db_date is None:
        today = datetime.date.today()
        db_date = "{0}-{1:02d}-{2}".format(today.year, today.month, today.day)

    tuple = (script_id, user_id, db_date, completed)
    
    cursor.execute("INSERT INTO sanitizedthis.requests (script_id,user_id,date,completed) VALUES (%s,%s,%s,%s);", tuple)
    
    mydb.commit()
    mydb.close()



if __name__ == "__main__":
    host = "localhost"
    username = "sanitizedthis"
    password = "sanitizedthis"
    
    db_name = "sanitizedthis"
    
    script_id = 2
    user_id = 1
    
    completed = 0
    
    db_insert(host, username, password, db_name, script_id, user_id, completed)


