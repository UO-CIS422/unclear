"""
TEMPORARY: Adding this to git version control because otherwise
I don't see how to copy on heroku before starting service. 

CONFIG module
We put here things that we might vary
depending on which machine we are running
on, or whether we are in debugging mode, etc.
"""
COOKIE_KEY = "A random string would be better"
DEBUG = True
PORT = 5000  # The default Flask port; change for shared server machines
