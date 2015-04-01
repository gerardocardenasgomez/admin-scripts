#!/usr/bin/env bash
# The first arg should be a file extension e.g. py or sh
# This script then goes through all files it finds and does a sed
# replacement on the WORDLIST to "sanitizedthis"

FILELIST=$(ls *.$1)
WORDLIST="list here"

for FILE in $FILELIST; do
    for WORD in $WORDLIST; do
        sed -i "s/$WORD/sanitizedthis/g" $FILE
        echo $?
    done
done
