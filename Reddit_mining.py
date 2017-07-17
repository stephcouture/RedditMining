# Script for Reddit data mining. This script will download datas from a given subreddit account, 
# and insert them into an sqlite database (reddit.sqlite).
#
# Arguments : RedditMining [Name of subreddit] [client_id] [client_secret] 
# Where [client_id] and [client_secret] can be found on your reddit account.
#
# The script will produce a database reddit.sqlite, that you can view (and manipulate with tools
# such as the SQLITEManager plugin in Firefox : https://addons.mozilla.org/fr/firefox/addon/sqlite-manager/
# 
# Created by Stéphane Couture
# scouture@yorku.ca


import praw
import sqlite3
import sys

subreddit_name = sys.argv[1]


# Getting arguments from command line to connect subreddit account
my_subreddit = sys.argv[1]  # Name of subreddit
my_client_id = sys.argv[2]  # Client id
my_client_secret = sys.argv[3] #client secret
my_user_agent = 'Python tryout script'


# Connect to subreddit
# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
reddit = praw.Reddit(client_id=my_client_id,
                     client_secret=my_client_secret,
                     user_agent=my_user_agent)

print(reddit.read_only)  # Output: True is connected

# Open or create the detabase. 
conn = sqlite3.connect('reddit.sqlite')
c = conn.cursor()

# Create the table submission and comment, if they do not exists
c.execute("CREATE TABLE IF NOT EXISTS submission (Title text, Submission_id string, User string, Timestamp integer, Body text)")
c.execute("CREATE TABLE IF NOT EXISTS comment (submission_id integer, Comment_id string, Parent_id string, Timestamp integer, User string, Body text)")
conn.commit() 

#Find the oldest submission here. This is usuful if you want to update the database. More testing needs to be done. 
c.execute("select min(Timestamp) from submission")
earliest = c.fetchone()[0]
print(earliest)

print (my_subreddit);
all_submissions = reddit.subreddit(my_subreddit).submissions(None, earliest)
#all_submissions = reddit.subreddit(my_subreddit).submissions()
      
for submission in all_submissions:
    if ((earliest is None) or (submission.created < earliest)) :  # for some reason, we don't get the earliest.

        # Insert submission data in the database
        c.execute("INSERT INTO submission (Title, Submission_id, User, Timestamp, Body) \
        VALUES (?,?,?,?,?)", (submission.title,
                              submission.id,
                              submission.author.name,
                              submission.created,
                              submission.selftext))
    
        conn.commit() 
        print(str(submission.created) +" -  id: "+ str(submission.id))
 
        # Get the comments a the specific submission
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            # print(vars(comment))  // to test
            # For JSON Reddit, see : https://github.com/reddit/reddit/wiki/JSON
            
            # Put them in the database        
            c.execute("INSERT INTO comment (submission_id, Comment_id, Parent_id, Timestamp, User, Body) \
                VALUES (?,?,?,?,?, ?)", (submission.id,
                                      comment.id,
                                      comment.parent_id,
                                      comment.created,
                                      "None" if comment.author is None else comment.author.name,
                                      comment.body))
            
            

print("Fin du script")

conn.close()
