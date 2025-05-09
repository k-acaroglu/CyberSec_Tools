#!/usr/bin/env python

import requests

def request(url):
    try:
       return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "google.com"

with open("/root/PycharmProjects/crawler/subdomains-wordlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip() # Strip all the \n or the white space on every line
        # target_url + "/" + word can be used to return directories of a website
        test_url = word + "." + target_url # test_url gives mail.google.com, which exists, but there are no responses??
        response = request(test_url) # response returns none?? Why????
        print(response)
        if response:
            print("[+] Discovered subdomain! --> " + test_url)