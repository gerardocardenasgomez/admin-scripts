# Dash_Submit.py

TODO: Allow for an append option.

## Examples

./dash_submit.py update --label=login_text --from-file=logs.txt --label-type=list --host=testing  
./dash_submit.py update --label=aide_status --label-type=text --host=testing --text=0  
./dash_submit.py update --label=status --label-type=text --host=testing --text=no  

## Config File

--config=/path/here

TODO: In future versions, this will not be necessary if the config file is in the same location as the script.

## URL

--url=http://url.here

This can be set in the config file as:

[data]
url=http://url.here

## Auth Token

--auth_token=token

This can be set in the config file as:

[data]
auth_token=token

This is required--Dashing will return a not authorized error if this is not set; the script by default will send an auth_token of None.

Note that it is more secure to place the auth_token in a config file that is only readable by root. Other users may be able to see the process arguments so it is not adviable to pass it as an argument to the script.
