#!/bin/bash
# Skeleton Script by Gerardo@GerardoBSD.com
# Version 1.1
#
set -euo pipefail
IFS=$'\n\t'

# Do not change thesse values
# GLOBAL VARIABLES
success='1'
# Anything written to temp_file will be deleted in the cleanup function
temp_file=$(mktemp)
# Help menu should not create any files at all
help_status='0'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# --USER OPTIONS--
# 
# # If you want to keep logs, change this value:
log_file=$temp_file
#
# # Change verbose here or with the -v option
verbose='0'
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#
# This function will run at the end
# Place any clean-up code here
#
function cleanup 
{
    
    # Help menu doesn't create any files at all; exit right away!
    if [[ "$help_status" -eq '1' ]]; then
        exit 0
    fi

    # If the script is successful, success should equal 1
    if [[ "$success" -eq '1' ]]; then

        # We made it here successfully
        echo "Perform a safe cleanup"

    elif [[ $"success" -eq '0' ]]; then

        # Something went wrong!
        echo "Perform nuclear cleanup"
        echo "Send an alert"
    
    else
        
        # Who knows what happened
        echo "Something went wrong?"

    fi

    # Clean up the temporary file
    rm -f $temp_file

    # User-defined clean-up tasks:
    # Here
}
trap cleanup EXIT
#
# Finish clean up function--bye!

#
# Set up logging platform
#
function log_platform()
{
    method=$1
    message=$2
    
    if [[ "$method" == 'ALERT' ]] || [[ "$method" == 'ALL' ]]; then
        echo "Method: $method Message: $message"
    fi

    if [[ "$method" == 'FILE' ]] || [[ "$method" == 'ALL' ]]; then
        echo "Method: $method Message: $message"
    fi
}
#
# Finish logging platform

#
# Get arguments
#
while getopts l:v:h var
do
    case "$var" in
        l) log_file=$OPTARG;;
        v) verbose='1';;
        h)  echo "$0: -v verbose, -l <file> log file, -h help"; help_status='1'; 
            # User Code here
            echo "$0: Help Menu"
            # End User Code
            exit 0;;
    esac
done 

# Code here
echo "My actions here" && success='1'
my_exit_code=$?

echo "${@: -1}"

if [[ "$my_exit_code" == 0 ]]; then
    log_platform 'ALERT' "The action was succesfully completed"
else
    log_platform 'FILE' "The action failed omg"
fi
