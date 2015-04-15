import json
import re
import urllib2
import xml.etree.ElementTree as ET

def recent_post(url):
    response = urllib2.urlopen(url)
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

    return blog_title, entry_title, latest_post

def recent_commit(url):
    response = urllib2.urlopen(url)
    data = response.read()

    decoded = json.loads(data)

    commit_msg  = decoded[0]['commit']['message']
    commit_date = decoded[0]['commit']['committer']['date']
    commit_url  = decoded[0]['html_url']

    return commit_msg, commit_date, commit_url
