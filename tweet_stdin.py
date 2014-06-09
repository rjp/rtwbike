import sys
import codecs
import json
import os
from twython import Twython

sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
tweet_this = sys.stdin.readlines()

apis = None
with open(os.getenv('HOME', '/tmp') + '/.apis', encoding="utf-8") as file:
    apis = json.load(file)

consumer_key=apis['twitter']['apps']['rtwapp']['api_key']
consumer_secret=apis['twitter']['apps']['rtwapp']['api_secret']
access_token=apis['twitter']['users']['zimpenfish_wf']['access_token']
access_secret=apis['twitter']['users']['zimpenfish_wf']['access_secret']

twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

twitter.update_status(status=tweet_this)
