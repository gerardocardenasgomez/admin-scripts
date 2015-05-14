#!/bin/bash
# Author: Gerardo Cardenas-Gomez
# Version 0.0.3
# Future plans: Added automatic uploading to Amazon S3
#               Appending to tempfile commands still look ugly
#
#
# Sanitize this section!
#
username=username                               # Make it easy to scrub sensitive data
email=email                                     # Make it easy to scrub sensitive data
bucketname=bucketname                           # Amazon S3 bucket, sanitized
bucketfolder=bucketfolder                       # Amazon S3 folder in bucket, sanitized
#
# Sanitize this section!
#

tempfile=$(mktemp)                              # Create the file that will be emailed

hostname=$(hostname)                            # So digging for the correct host isn't necessary


date=$(date +"%Y%m%d")                          # Year-Month-Day format
rand=$(echo -$RANDOM)                           # To help prevent duplicate files
filename=/home/$username/BACKUPS/backup$date$rand.tar.gz


echo -e "\nLogged in:" >> $tempfile
who >> $tempfile
echo -e "\nlast output:" >> $tempfile
last >> $tempfile

echo -e "\nUpdate information:" >> $tempfile

                                                # Print info about regular and security updates
apt_updates=$(/usr/lib/update-notifier/apt-check 2>&1)
reg_updates=$(cut -d ';' -f 1 <<< $apt_updates)
sec_updates=$(cut -d ';' -f 2 <<< $apt_updates)

echo -e "\nThere are $reg_updates regular updates available." >> $tempfile
echo -e "\nThere are $sec_updates security updates available." >> $tempfile

echo -e "\nBACKUP INFORMATION" >> $tempfile
                                                # Errors get appended to $tempfile
tar -cvpzf $filename /var/www 2>> $tempfile
exitcode=$?

if [ $exitcode = "0" ]; then
    chmod 400 $filename                         # Backup file contains sensitive data!

    echo -e "\nAWS S3 uploader" >> $tempfile
    aws s3 cp $filename s3://$bucketname/$bucketfolder/ 2>> $tempfile 

    echo "Successful backup from $hostname!" >> $tempfile
    mail -s "Backup: $hostname on $date" $email  < $tempfile
else
    echo "WARNING: FAILED BACKUP FROM $hostname with exit code of $exitcode" >> $tempfile
    mail -s "FAILED Backup: $hostname on $date" $email < $tempfile
fi
