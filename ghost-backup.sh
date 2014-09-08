#!/bin/bash
# Author: Gerardo Cardenas-Gomez
# Version 0.0.1
# Future plans: Clean up the spacer stuff
#               Add functions instead
#
TEMPFILE=$(mktemp)                              # Create the file that will be emailed
hostname=$(hostname)                            # So digging for the correct host isn't necessary
username=username                               # Make it easy to scrub sensitive data
email=email                                     # Make it easy to scrub sensitive data
spacer="================="

date=$(date +"%Y%m%d")                          # Year-Month-Day format
rand=$(echo -$RANDOM)                           # To help prevent duplicate files
filename=/home/$username/BACKUPS/backup$date$rand.tar.gz

echo "Logged in:"
who >> $TEMPFILE
echo "$spacer" >> $TEMPFILE
echo "last output:"
last >> $TEMPFILE
echo "$spacer" >> $TEMPFILE

                                                # Print update info from Ubuntu motd
if [ -e "/var/lib/update-notifier/updates-available" ]; then
    cat /var/lib/update-notifier/updates-available >> $TEMPFILE
else
    echo "No updates available, yay!" >> $TEMPFILE
fi
echo "$spacer" >> $TEMPFILE

echo "BACKUP INFORMATION" >> $TEMPFILE
echo "$spacer" >> $TEMPFILE
echo "$spacer" >> $TEMPFILE
echo "$spacer" >> $TEMPFILE

                                                # Errors get appended to $TEMPFILE
tar -cvpzf $filename /var/www/ 2>> $TEMPFILE
exitcode=$?

if [ $exitcode = "0" ]; then
    chmod 400 $filename                         # Backup file contains sensitive data!

    echo "Successful backup from $hostname!" >> $TEMPFILE
    mail -s "Backup: $hostname on $date" $email  < $TEMPFILE
else
    echo "WARNING: FAILED BACKUP FROM $hostname with exit code of $exitcode" >> $TEMPFILE
    mail -s "FAILED Backup: $hostname on $date" $email < $TEMPFILE
fi
