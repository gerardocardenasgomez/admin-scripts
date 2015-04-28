#!/usr/bin/env python
from flask import Flask, request, render_template
import blogimport
import mongocache

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://gerardobsd.com:443/rss/'
    blog_title, entry_title, latest_post = mongocache.db_cache(url, blog=True)

    url = 'https://api.github.com/repos/gerardocardenasgomez/admin-scripts/commits?since=2015-04-11T11:59:00Z'
    commit_msg, commit_date, commit_url = blogimport.recent_commit(url, git=True)

    output_text = "<h1>" + blog_title + "</h1>"
    output_text = output_text + "<h2>" + entry_title + "</h2>"
    output_text = output_text + "<p>" + latest_post + "</p>"

    output_text = output_text + "<h1>" + "Recent git Commit" + "</h1>"
    output_text = output_text + "<p>" + commit_msg + "</p>"
    output_text = output_text + "<p>" + commit_date + "</p>"
    output_text = output_text + """<p> <a href="{0}" alt="Recent Commit">{1}</a></p>""".format(commit_url, commit_url)

    return output_text 

if __name__ == '__main__': 
    app.run(debug=False)
