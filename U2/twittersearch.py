#!/usr/bin/python2

import json
import urllib2
import sys
from HTMLParser import HTMLParser
from base64 import b64encode

""" We need to authenticate to twitter API """
key = "R5aO3h3jaujNbzkoQq4m7aUcV"
secret = "QQ6m7afFLLdJWFynlxODLv7Gg4ZPIGOo7vH0Nk9ja7t5riwSmk"
enckey = b64encode(key + ":" + secret)

auth = urllib2.Request("https://api.twitter.com/oauth2/token")
auth.add_header("Authorization", "Basic " + enckey)
auth.add_header("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
auth.add_data("grant_type=client_credentials")

response = urllib2.urlopen(auth).read()
dict = json.loads(response)
access_token = dict['access_token']

""" now we can use GET to search """
params = "count=100&q=" + sys.argv[1]
search_req = urllib2.Request("https://api.twitter.com/1.1/search/tweets.json?"+params)
search_req.add_header("Authorization", "Bearer " + access_token)
response = json.loads(urllib2.urlopen(search_req).read())
tweets = response['statuses']

h = HTMLParser()
for tweet in tweets:
    text = tweet['text']
    decoded = h.unescape(text)
    print decoded

        

