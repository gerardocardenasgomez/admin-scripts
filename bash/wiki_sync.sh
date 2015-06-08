#!/usr/bin/env bash
base_dir=/var/lib/dokuwiki/data/pages
target_dir=$1
file_list=$(ls -1 $1)

for file in $file_list; do
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
