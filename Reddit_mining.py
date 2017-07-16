import praw
import sqlite3
import sys

subreddit_name = sys.argv[1]


my_subreddit = sys.argv[1]
my_client_id = sys.argv[2]
my_client_secret = sys.argv[3]
my_user_agent = 'Python tryout script'


# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
reddit = praw.Reddit(client_id=my_client_id,
                     client_secret=my_client_secret,
                     user_agent=my_user_agent)

print(reddit.read_only)  # Output: True

# Open or create the detabase. 
conn = sqlite3.connect('reddit.sqlite')
c = conn.cursor()

# Create the table submission
c.execute("CREATE TABLE IF NOT EXISTS submission (Title text, Submission_id integer, User integer, Timestamp datetime, Body text)")

print (my_subreddit);
all_submissions = reddit.subreddit(my_subreddit).submissions()
      
for submission in all_submissions:
    # Insert a row of data
    #print(vars(submission.author))
    c.execute("INSERT INTO submission (Title, Submission_id, User, Timestamp, Body) \
    VALUES (?,?,?,?,?)", (submission.title,
                          submission.id,
                          submission.author.name,
                          submission.created,
                          submission.selftext))
    
    conn.commit() 
    print(str(submission.created) +" -  id: "+ str(submission.id))
 
    
    #submission.comments.replace_more(limit=0)
    #for comment in submission.comments.list():
        # print(vars(comment))  



conn.close()
