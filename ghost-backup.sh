#!/bin/bash
# Author: Gerardo Cardenas-Gomez
# Version 0.0.3
# Future plans: Added automatic uploading to Amazon S3
#               Appending to TEMPFILE commands still look ugly
#
TEMPFILE=$(mktemp)                              # Create the file that will be emailed
NOTIFIERFILE=/var/lib/update-notifier/updates-available

hostname=$(hostname)                            # So digging for the correct host isn't necessary
username=username                               # Make it easy to scrub sensitive data
email=email                                     # Make it easy to scrub sensitive data

date=$(date +"%Y%m%d")                          # Year-Month-Day format
rand=$(echo -$RANDOM)                           # To help prevent duplicate files
filename=/home/$username/BACKUPS/backup$date$rand.tar.gz

bucketname=bucketname                           # Amazon S3 bucket, sanitized
bucketfolder=bucketfolder                       # Amazon S3 folder in bucket, sanitized

echo -e "\nLogged in:" >> $TEMPFILE
who >> $TEMPFILE
echo -e "\nlast output:" >> $TEMPFILE
last >> $TEMPFILE

echo -e "\nUpdate information:" >> $TEMPFILE
                                                # Print update info from Ubuntu motd
if [ -e $NOTIFIERFILE ]; then
    FSIZE=$(stat --printf="%s" $NOTIFIERFILE)   # Notifier file is empty if there are no updates
    if [ $FSIZE -gt 1 ]; then
        cat $NOTIFIERFILE >> $TEMPFILE
    else
        echo "There are no new updates available!" >> $TEMPFILE
   fi
fi

echo -e "\nBACKUP INFORMATION" >> $TEMPFILE
                                                # Errors get appended to $TEMPFILE
tar -cvpzf $filename /var/www 2>> $TEMPFILE
exitcode=$?

if [ $exitcode = "0" ]; then
    chmod 400 $filename                         # Backup file contains sensitive data!

    echo -e "\nAWS S3 uploader" >> $TEMPFILE
    aws s3 cp $filename s3://$bucketname/$bucketfolder 2>> $TEMPFILE 

    echo "Successful backup from $hostname!" >> $TEMPFILE
    mail -s "Backup: $hostname on $date" $email  < $TEMPFILE
else
    echo "WARNING: FAILED BACKUP FROM $hostname with exit code of $exitcode" >> $TEMPFILE
    mail -s "FAILED Backup: $hostname on $date" $email < $TEMPFILE
fi
