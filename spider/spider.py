#!/usr/bin/env python

import requests
import re
import urllib.parse as urlparse

target_url = "https://zsecurity.org"
target_links = []

def extract_links_from(url):
    response = requests.get(url) # response.content returns the html of website
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0] # # before links still load the same html

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)

crawl(target_url)