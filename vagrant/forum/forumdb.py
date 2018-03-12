# "Database code" for the DB Forum.

import psycopg2
import datetime
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]
DBNAME = "dbname=forum"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  all_posts = []
  db = psycopg2.connect(DBNAME)
  cur = db.cursor()
  cur.execute("select content, time from posts order by time desc")
  list_posts = cur.fetchall()
  for text, date in list_posts:
    all_posts.append((bleach.clean(text), date)) 
  db.close()
  return all_posts
  # return reversed(POSTS)

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  # POSTS.append((content, datetime.datetime.now()))
  db = psycopg2.connect(DBNAME)
  cur = db.cursor()
  cur.execute("insert into posts values (%s)", (content,))
  db.commit()
  db.close()


