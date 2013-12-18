#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from django.utils import simplejson as json
from tweepylogin import LoginHandler, OauthHandler
from tweepymodels import Agent, Config
import tweepy
import sys
import os
import urllib
import pywapi
import pprint
from optparse import OptionParser
from xml.dom.minidom import parse
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import datetime
import urllib2



class TweetLog(db.Model):
    username = db.StringProperty()
    replied_on = db.DateTimeProperty(auto_now=True)

    @staticmethod
    def get(tweet_id):
        tweet_id = str(tweet_id)
        tweetlog = TweetLog.get_by_key_name(tweet_id)
        return tweetlog

    @staticmethod
    def set(tweet_id, username):
        Config(key_name=str(tweet_id),
               username=username
               ).put()

	
	
class WeatherInfo(webapp.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler('mM6qxghuXMaGH86lHVVOWA','JOM29LabfIJ6v8ZccVwchPFWomapYyvlTeQ0uwBelQ')
        auth.set_access_token('400026591-m4lMAuCtsw5xDGQ9suPsgqSr4ykwYWJClmXOdxpn', '7xjgEqqbdMmcwtQ0XRcgdQ65ecVdi8TYWnDH1mtoHs')
        api = tweepy.API(auth)

	location = 'Mataram'
	resGoogle = pywapi.get_weather_from_google(location)
	resYahoo = pywapi.get_weather_from_yahoo('IDXX0032', 'metric')
	time = datetime.datetime.utcnow() + datetime.timedelta(hours = 8)
	
	visibility = resYahoo['atmosphere']['visibility'] + ' km'
	sunrise = resYahoo['astronomy']['sunrise']
	sunset = resYahoo['astronomy']['sunset']
	
	update = time.strftime("%Y-%m-%d, %H:%M") + ' WITA: ' + location + ' ' + resGoogle['current_conditions']['condition'] + ', ' + resGoogle['current_conditions']['temp_c'] + ' C' + ', ' + resGoogle['current_conditions']['humidity']  +', ' +  resGoogle['current_conditions']['wind_condition'] + ', Visibility: ' + visibility + ', Sunrise: ' + sunrise + ', Sunset: ' + sunset
	self.response.out.write(update)

	
        api.update_status(update)
		

class WeatherWunderground(webapp.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler('wJynZvsXCJDbxFavJZMuvQ','Ua9HSGqJntKpBMfTYuldjuplo3XUlC3QovTn7EOQ')
        auth.set_access_token('400026591-XCtPsJABBP5MGF13Q4xFVXZurRcVtCcJ0VaU9Dr5', '635W0s9PIVYxlVktp0hWiNkBfNS4ntuW7c2thGsp8')
        api = tweepy.API(auth)
		
	location = 'Mataram'
	f = urllib2.urlopen('http://api.wunderground.com/api/da229b2203c824d3/geolookup/conditions/q/IA/' + location +'.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	
	resYahoo = pywapi.get_weather_from_yahoo('IDXX0032', 'metric')
	
	time = datetime.datetime.utcnow() + datetime.timedelta(hours = 8)
	location = parsed_json['location']['city']
	current = parsed_json['current_observation']['weather']
	temp_c = parsed_json['current_observation']['temp_c']
	humidity = parsed_json['current_observation']['relative_humidity']
	visibility = parsed_json['current_observation']['visibility_km']
	f.close()
	
	sunrise = resYahoo['astronomy']['sunrise']
	sunset = resYahoo['astronomy']['sunset']
	wind = resYahoo['wind']['speed'] + ' km'
	winddir = resYahoo['wind']['direction'] 
	
	update = time.strftime("%Y-%m-%d, %H:%M") + ' WITA : ' + location + ' ' + current + ' ' + str(temp_c) +' C' + ', Humidity: ' + humidity  +', ' + ' Visibility: ' + visibility + ' km'
	update = update + ', Wind: ' + wind  + ', Sunrise: ' + sunrise + ', Sunset: ' + sunset
	self.response.out.write(update)
	api.update_status(update)
  

def main():
    application = webapp.WSGIApplication([
            ('/', WeatherWunderground)],
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
