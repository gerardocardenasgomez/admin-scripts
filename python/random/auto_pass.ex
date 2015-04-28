spawn ./pass_input.py [lindex $argv 0]
set password [lindex $argv 1]
expect "Password:"
send "$password\r"
expect "Password:"
send "$password\r"
send_user "Action complete!"
expect eof
