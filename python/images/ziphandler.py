#!/usr/bin/env python
# This script simply takes in all zip archives, extracts them, and removes the zip archive.
import glob
import zipfile
import os

for zipArchive in glob.glob('*.zip'):
    if zipfile.is_zipfile(zipArchive):
        with zipfile.ZipFile(zipArchive) as zf:
            zf.extractall(".")
            os.remove(zipArchive)
