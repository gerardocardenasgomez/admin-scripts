#!/usr/bin/env python
import getpass
import sys

user_name = sys.argv[1]

first_user_response     =   getpass.getpass("Password: ")
second_user_response    =   getpass.getpass("Password: ")

if first_user_response == second_user_response:
    with open("test.txt", "w") as f:
        f.write(user_name + "\n")
        f.write(first_user_response + "\n")
    sys.exit(0)
else:
    print "Passwords do not match!"
    sys.exit(1)
