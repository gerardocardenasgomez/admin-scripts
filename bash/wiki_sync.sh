#!/usr/bin/env bash
# This script is meant to check for differences between the wiki pages
#   and the git repo for my wiki. 
# If it finds any differences, it will copy the files fom the wiki
#   to the repo for the wiki. This should onl be used when the wiki
#   is up-to-date but the repo is not. Otherwise, you will undo
#   changes in the repo!
# This current version ignores the README.md file in the repo
#   that would otherwise cause some unnecessary output. The
#   README.md file is not needed in the wiki directory.
#

base_dir=/var/lib/dokuwiki/data/pages
target_dir=$1
file_list=$(ls -1 $1)

for file in $file_list; do
    if [[ $file == *"README.md"* ]]; then
        continue
    fi

    result=$(diff $base_dir/$file $target_dir/$file)
    exit_code=$?
    if [[ "$exit_code" -ne 0 ]]; then
        cp $base_dir/$file $target_dir/$file
        exit_code=$?
        
        if [[ "$exit_code" -eq 0 ]]; then
            echo "$file copy successful"
        else
            echo "Something went wrong with $file"
        fi
    fi
done
