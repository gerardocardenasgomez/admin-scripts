#!/usr/bin/env python
import re
from flask import Flask, request
import pymongo
import urllib2
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    return "welcome, hi"

@app.route('/user/<name>')
def user(name):
    dangerous_string = name

    clean_string = re.sub('\W+', '', dangerous_string)

    if not clean_string.isalnum():
        return "No special characters allowed"

    user_agent = request.headers.get('User-Agent')

    connection = pymongo.MongoClient('localhost', 27017)
    db = connection.test
    names = db.names

    results = names.find_one({ "name" : clean_string })

    if results:
        page_output = "Name: {0} Age: {1}".format(results["name"], results["age"])

        page_output = page_output + " " + user_agent

        return page_output
    else:
        return "User not found, sorry."

@app.route('/overview')
def overview():
    response = urllib2.urlopen('https://gerardobsd.com:443/rss/')
    data = response.read()
    
    root = ET.fromstring(data)
    
    titles = []
    for item in root.iter('title'):
        titles.append(item)

    blog_title = titles[0].text
    entry_title = titles[1].text

    blog_desc = []

    for item in root.iter('description'):
        blog_desc.append(item)

    latest_post = blog_desc[1].text

    start_tag_pattern = re.compile(r'\<p\>')
    end_tag_pattern = re.compile(r'\<\/p\>')

    start_index = re.search(start_tag_pattern, latest_post).start()
    start_index = start_index + 3

    end_index = re.search(end_tag_pattern, latest_post).start()

    latest_post = latest_post[start_index:end_index]

    output_text = "<h1>" + blog_title + "</h1>"
    output_text = output_text + "<h2>" + entry_title + "</h2>"
    output_text = output_text + "<p>" + latest_post + "</p>"

    return output_text 

if __name__ == '__main__': 
    app.run(host='', port=8080, debug=True)
