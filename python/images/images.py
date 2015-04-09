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

def checkPath(dir):
    """Raise an error if the directory does not exist"""
    try:
        if not os.path.isdir(dir):
            raise IOError()
    except IOError:
        print "Error: Directory does not exist"
        sys.exit(1)

def getHash(fname):
    """Hash a file using MD5 and return the result hash"""
    file = open(fname, 'rb')
    h = hashlib.md5()
    h.update(file.read())
    return h.hexdigest()

def db_mtime(stats):
    """Get a file's modification time and return it in a database-friendly format"""
    mtime = time.gmtime(stats.st_mtime)
    str_time = datetime.date(mtime.tm_year, mtime.tm_mon, mtime.tm_mday)
    return str_time

def insertImage(stats, fname, submitted, cursor, md5hash):
    """Insert an image into a MySQL Database

    First, check that the image is not already in the Database by searching for its MD5 hash

    If the image is not already in the database, insert it. These are the fields that are inserted:

    - id int(12) NOT NULL AUTO_INCREMENT UNIQUE
    - fname VARCHAR(255) NOT NULL
    - size int(25) NOT NULL
    - modified DATE
    - submitted DATE
    - hash VARCHAR(64)

    The modified field comes from the operating system and is the file's "modified" attribute.
    """

    command = cursor.execute("""SELECT * FROM imgtbl WHERE hash=%s""", (md5hash,))
    results = cursor.fetchall()
    
    if not results:
        sqlmtime = db_mtime(stats)
        fsize = statinfo.st_size

        # Use a tuple to safely escape special characters
        tuple = (fname, fsize, sqlmtime, submitted, md5hash)

        cursor.execute("""INSERT INTO imgtbl(fname,size,modified,submitted,hash) VALUES(%s,%s,%s,%s,%s);""", tuple)
    elif results:
        print "Picture {0} is already in the DB!".format(fname)
    else:
        print "Error?"

# getBasepath will check that the directory exists
basepath = sys.argv[1] 
checkPath(basepath)
    
#MySQL DB Variables
host = "localhost"
user = "pyimages"
passwd = "pypass"
db = "images"
#MySQL DB Connection
mydb = mysql.connect(host, user, passwd, db)
#MySQL DB Cursor
cursor = mydb.cursor()

basepath = '/home/excom/testing/images'

imgExtensions = ("jpg", "peg", "png", "gif")

# Submitted Date
submitted = datetime.date.today()

for fname in os.listdir(basepath):

    path = os.path.join(basepath, fname)

    if path[-3:] in imgExtensions:      # Check if it is an approved extension
        statinfo = os.stat(path)
        md5hash = getHash(path)
        insertImage(statinfo, fname, submitted, cursor, md5hash)

cursor.close()
mydb.commit()
mydb.close()
