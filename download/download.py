#!/usr/bin/env python
import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file: # wb = write binary
        out_file.write(get_response.content)

download("https://media.tenor.com/QhGPwGiOBY0AAAAe/laugh-pointing.png")
