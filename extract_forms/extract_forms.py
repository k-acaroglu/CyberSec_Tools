#!/usr/bin/env python

import requests
from BeautifulSoup import BeautifulSoup # This library is perfect for extracting html
import urlparse

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnetionError:
        pass

target_url = "enter url here with a form"
response = request(target_url) # This .content returns the html of the website

parsed_html = BeautifulSoup(response.content) # Access different parts of the html
forms_list = parsed_html.findAll("form") # This function can return any html tag as a list
# Important values: action, method, name (under input tag)

# For getting elements, use for loop. For getting attributes, use element.get("attribute")
for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action) # Joins the full url to post
    method = form.get("method")

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"

        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)