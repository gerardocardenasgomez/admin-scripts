#!/usr/bin/env python
import re
import string
import sys
import os

orphan_links = []
orphan_files = []
temp_store   = []

link_file   = sys.argv[1]
target_dir  = sys.argv[2]

# link_pattern will be used to search for the links
#   which look like: [[<link here>]]
link_pattern            = re.compile(r'(\[\[\w*[-]*\s*[\(]*\s*\w*[\)]*\]\])')

# parens_replace_pattern will only replace an opening parens
#   that is within a word with an underscore: [[Node(Chef)]] --> [[Node_Chef)]]
parens_replace_pattern  = re.compile(r'(?!\w)[\(](?=\w)')

# char_replace_pattern will remove characters [, ], (, and )
char_replace_pattern    = re.compile(r'[\(\[\]\)]')

# unders_replace_pattern will make sure there is only one underscore
unders_replace_pattern  = re.compile(r'(?=\w)_{2,}(?=\w)')

with open(link_file, "r") as f:
    for line in f:
        match = link_pattern.findall(line)

        if match:
            for item in match:
                result = parens_replace_pattern.sub('_', item)
                result = char_replace_pattern.sub('', result)
                result = result.replace(' ', "_")
                result = unders_replace_pattern.sub('_', result)
                orphan_links.append(result.lower())

orphan_files = [ f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir,f)) ]


for item in orphan_links:
    if (item + ".txt") in orphan_files:
        temp_store.append(item)

for item in temp_store:
    list_index = orphan_files.index((item + ".txt"))
    file_index = orphan_links.index(item)
    
    del(orphan_files[list_index])
    del(orphan_links[file_index])

print "----orphaned links:"
for item in orphan_links:
    print item

print "----orphaned files:"
for item in orphan_files:
    print item
