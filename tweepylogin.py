"""
Twitter Login helper for Google App Engine

Usage:
In main.py (or any file where you are implementing webapp)

- from tweepylogin include *
- from tweepymodels import Agent

In URL mapping, drop these two lines:
- ('/login', LoginHandler),
- ('/oauth/callback', OauthHandler),

And finally, to get the oauth keys:
- oauth_key, oauth_secret = Agent.get('username')

To get an authenticated API:

- auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
- auth.set_access_token(oauth_key, oauth_secret)
- api = tweepy.API(auth)

Now you can use:
- api.update_status("It's Alive!")

You'll get the consumer_key and consumer_secret from dev.twitter.com

NOTE: Look out for "IMPORTANT" a few lines below...

http://bitbucket.org/hiway
"""

import tweepy
import os

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import users
from appengine_utilities import sessions

from tweepymodels import Config, RequestToken, Agent

# Get appname
from google.appengine.api.app_identity import get_application_id
appname = get_application_id()


# Figure out which URL to use for callback
# ================ IMPORTANT ================
# Update the port in "Dev" mode if you are playing with 
# more than one appengine apps.

if os.environ['SERVER_SOFTWARE'][:3] == "Dev":
    callback_url = 'http://localhost:8086/oauth/callback'
    # you must update this part here ^^^^
else:
    callback_url = 'http://%s.appspot.com/oauth/callback' %(appname)


def login_required(func):
    def wrapper(self, *args, **kw):
        session = sessions.Session()
        if not session.has_key("user_id"):
            self.redirect("/login")
        else:
            func(self, *args, **kw)

    return wrapper



class LogoutHandler(webapp.RequestHandler):
    def get(self):
        session = sessions.Session()
        session.delete_item("user_id")
        session.delete_item("screen_name")
        self.redirect("/")



class LoginHandler(webapp.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler(
                                    Config.get('consumer_key'),
                                    Config.get('consumer_secret'),
                                    callback_url
                                    )

        url = auth.get_authentication_url()

        r_token = RequestToken()
        r_token.set(auth.request_token.key, auth.request_token.secret)

        self.redirect(url)



class OauthHandler(webapp.RequestHandler):
    def get(self):
        oauth_token = self.request.get("oauth_token")
        oauth_verifier = self.request.get("oauth_verifier")

        r_token = RequestToken()
        oauth_secret = r_token.get(oauth_token)

        auth = tweepy.OAuthHandler(
                                    Config.get('consumer_key'),
                                    Config.get('consumer_secret'),
                                    callback_url
                                    )

        auth.set_request_token(oauth_token, oauth_secret)
        access_token = auth.get_access_token(oauth_verifier)

        api = tweepy.API(auth)
        twitteruser = api.me()
        Agent.set(twitteruser.screen_name,
              access_token.key,
              access_token.secret)

        session = sessions.Session()
        session["user_id"] = str(twitteruser.id)
        session["screen_name"] = twitteruser.screen_name

        self.redirect('/')
