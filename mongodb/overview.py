#!/usr/bin/env python
import re
from flask import Flask, request, render_template
import pymongo
import urllib2
import xml.etree.ElementTree as ET
import blogimport

app = Flask(__name__)

@app.route('/')
def index():
    blog_title = "Cars"
    entry_title = "bears"
    latest_post = "a bunch of text herehrhe"

    output_text = { "blog_title": blog_title,
                    "entry_title" : entry_title,
                    "latest_post" : latest_post}

    return render_template('latest_post.html',
                    blog_title  = blog_title,
                    entry_title = entry_title,
                    latest_post = latest_post)

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
    blog_title, entry_title, latest_post = blogimport.recent_post('https://gerardobsd.com:443/rss/')

    commit_msg, commit_date, commit_url = blogimport.recent_commit('https://api.github.com/repos/gerardocardenasgomez/admin-scripts/commits?since=2015-04-11T11:59:00Z')

    output_text = "<h1>" + blog_title + "</h1>"
    output_text = output_text + "<h2>" + entry_title + "</h2>"
    output_text = output_text + "<p>" + latest_post + "</p>"

    output_text = output_text + "<h1>" + "Recent git Commit" + "</h1>"
    output_text = output_text + "<p>" + commit_msg + "</p>"
    output_text = output_text + "<p>" + commit_date + "</p>"
    output_text = output_text + """<p> <a href="{0}" alt="Recent Commit">{1}</a></p>""".format(commit_url, commit_url)

    return output_text 

if __name__ == '__main__': 
    app.run(host='100.78.122.25', port=8080, debug=True)
