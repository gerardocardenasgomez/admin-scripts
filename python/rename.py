#!/usr/bin/env python
# This script takes in files with the '-' character and renames them
#   to whatever was in the third column.
# Only files with the format: "xx - xxxxxxxx" should be added to this script.

import string
import glob
import shutil

fileExt = ("jpg", "jpeg", "png", "gif")

for ext in fileExt:
    for pic in glob.glob('*[-]*.%s' % ext):
        result = string.split(pic)
        try:
            shutil.move(pic, result[2])
        except:
            print "Oops, something went horribly wrong!"
