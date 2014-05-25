#! /usr/bin/env python

import sqlite3
import sys
import os
import json
import re

dbfile = sys.argv[1]

conn = sqlite3.connect(dbfile)
c = conn.cursor()

# Some tweets have the wrong distances and we replace them
overrides = {}
c.execute("select tweet_id, distance from ignore_tweets")
for data in c.fetchall(): overrides[data[0]] = data[1]

c.execute("select tweet_id, tweet_date, tweet from tweets")
for tweet_data in c.fetchall():
    [tweet_id, tweet_date, tweet] = tweet_data
    # print(tweet_data)
    m = re.search('GPS log.*\s([0-9.]+)\s', tweet)
    if m:
        # print(m.group(1)) 
        distance = overrides.get(tweet_id, float(m.group(1)))
        c.execute("insert or ignore into distances (tweet_id, distance, date) values (?,?,?)", [tweet_id, distance, tweet_date])

conn.commit()
