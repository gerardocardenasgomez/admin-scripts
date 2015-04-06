#!/usr/bin/env python
import sendgrid

def sg_mailer(user_email, user_name, key_name, ip_addr, script_title, script_desc, script_link):
    sg_username = ''
    sg_password = ''
    
    sg = sendgrid.SendGridClient(sg_username, sg_password)
    message = sendgrid.Mail()
    
    message.set_from("Support@Tiplette.com")
    message.set_subject("Your Virtual Machine is Ready!")
    message.add_to(user_email)

    message.set_text = """
Hey, {0}!

Your Virtual Machine is now ready!

Log in using your "{1}" key.

IP Address: {2}

Your challenge is: {3}!

{4}

The link to your challenge is {5}
""".format(user_name, key_name, ip_addr, script_title, script_desc, script_link)

    status, msg = sg.send(message)

    return status
