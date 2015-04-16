import pymongo
import os
import blogimport
import json
import datetime

def db_cache(url, blog=False, git=False):
    mongo_host = os.environ['OPENSHIFT_MONGODB_DB_HOST']
    mongo_port = os.environ['OPENSHIFT_MONGODB_DB_PORT']

    mongo_user = os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
    mongo_pass = os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']

    connection = pymongo.MongoClient(mongo_host, int(mongo_port))
    connection.gccom.authenticate(mongo_user, mongo_pass)

    db = connection.gccom
    pydata = db.data

    if blog:
        try:
            results = pydata.find_one({"name" : "blog"})

            if not results:
                raise exception

            blog_title  = results["blog_title"]
            entry_title = results["entry_title"]
            latest_post = results["latest_post"]
            
            return blog_title, entry_title, latest_post

        except:
            blog_title, entry_title, latest_post = blogimport.recent_post(url)
            
            blog_data = {"name" : "blog", 
                        "blog_title" : blog_title,
                        "entry_title": entry_title,
                        "latest_post": latest_post,
                        "createdAt" : datetime.datetime.utcnow()}
            pydata.insert(blog_data)
            return blog_title, entry_title, latest_post

    if git:
        try:
            results = pydata.find_one({"name" : "git"})

            if not results:
                raise exception

            commit_msg  = results['commit_msg']
            commit_date = results['commit_date']
            commit_url  = results['commit_url']

            return commit_msg, commit_date, commit_url

        except:
            commit_msg, commit_date, commit_url = blogimport.recent_commit(url)
    
            commit_data = {"name" : "git",
                            "commit_msg"    : commit_msg,
                            "commit_date"   : commit_date,
                            "commit_url"    : commit_url,
                            "createdAt"     : datetime.datetime.utcnow()}
            pydata.insert(commit_data)
            return commit_msg, commit_date, commit_url

    if not git and not blog:
        return "System error", "Must set EITHER git or blog to True!", "100"
