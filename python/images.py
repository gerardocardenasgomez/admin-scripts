#!/usr/bin/env python
# This script should add any images in a directory to a MySQL database.
# It should make sure to only add jpg, jpeg, gif, and png images.
# It should check to make sure the file is not already in the database.
# Finally, it should add the image, its name, and date of creation.
import os
import time
import sys
import MySQLdb as mysql
import datetime
import hashlib

def insertImage(stats, fname, submitted, cursor):
    mtime = time.gmtime(stats.st_mtime)
    sqlmtime = datetime.date(mtime.tm_year, mtime.tm_mon, mtime.tm_mday)
    
    h = hashlib.md5()
    h.update(fname + str(sqlmtime))

    command = cursor.execute("""SELECT * FROM imgtbl WHERE hash='%s'""" % h.hexdigest())
    results = cursor.fetchall()
    
    if not results:
        statement = """INSERT INTO imgtbl(fname,size,modified,submitted,hash) """ \
            """VALUES('%s','%d','%s','%s','%s');"""  % (fname, statinfo.st_size, sqlmtime, submitted, h.hexdigest())
        cursor.execute(statement)
        print "added"
    elif results:
        print "Picture is already in the DB!"
    else:
        print "Error?"
    
#MySQL DB Variables
host = "localhost"
user = "user"
passwd = "pass"
db = "images"
#MySQL DB Connection
mydb = mysql.connect(host, user, passwd, db)
#MySQL DB Cursor
cursor = mydb.cursor()


basepath = '/var/www/data/images'

scriptName = sys.argv[0]					# Do not add the script to the database
scriptPath = basepath + scriptName[1:]		# Do not add the script to the database

imgExtensions = ("jpg", "peg", "png", "gif")

# Submitted Date
submitted = datetime.date.today()
# End of Submitted Date

for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if path[-3:] in imgExtensions:      # Check if it is an approved extension
        statinfo = os.stat(path)
        insertImage(statinfo, fname, submitted, cursor)

cursor.close()
mydb.commit()
mydb.close()
