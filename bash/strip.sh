#!/usr/bin/env bash

fixed_input=""

for word in $@; do
    echo $word
    back=$(echo $word | tr -d '"')
    fixed_input+=$back
    fixed_input+=" "
done

echo $fixed_input
