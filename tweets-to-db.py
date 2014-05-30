#! /usr/bin/env python

import sqlite3
import sys
import os
import sys
import codecs
from datetime import datetime
import pytz

utc = pytz.utc

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

dbfile = sys.argv[1]
tweets = sys.argv[2]

conn = sqlite3.connect(dbfile)
c = conn.cursor()

with open(tweets, encoding="utf-8") as file:
    for line in file:
        (id, datetimetz, user, rest) = line.split(' ', 3)
        print("%s,%s,[%s]" % (id, datetimetz, rest))
        tweet_text = rest.rstrip('\r\n')
        c.execute('insert or ignore into tweets values (?,?,?)', [id, datetimetz, tweet_text])
    conn.commit()
conn.close()
