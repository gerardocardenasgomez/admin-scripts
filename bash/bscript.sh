#!/usr/bin/env bash

DIR=$1
DATE=$(date +%Y%m%d)
HOMEDIR=~
OUTPUTDIR=$HOMEDIR
VERBOSE=0

while getopts "hvo:b:" opt; do
    case "$opt" in
    h)
        echo "-h for help, -o for output file, -v for verbose, -b for target dir to back up"
        exit 0
        ;;
    v)
        VERBOSE=1
        ;;
    o)
        OUTPUTDIR=$OPTARG
        ;;
    b)
        DIR=$OPTARG
        ;;
    esac
done

TARNAME=$(basename $DIR)

if [ -d $DIR ]; then
    tar cvf $OUTPUTDIR/$TARNAME-$DATE $DIR
fi
