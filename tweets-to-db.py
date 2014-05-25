#! /usr/bin/env python

import sqlite3
import sys
import os

dbfile = sys.argv[1]
tweets = sys.argv[2]

conn = sqlite3.connect(dbfile)
c = conn.cursor()

with open(tweets) as file:
    print(file)
    for line in file:
        print(line.split(' ', 5))
        (id, date, time, timezone, user, rest) = line.split(' ', 5)
        print("%s,%s %s %s,[%s]" % (id, date, time, timezone, rest))
        tweet_text = rest.rstrip('\r\n')
        c.execute('insert or ignore into tweets values (?,?,?)', [id, date+' '+time+' '+timezone, tweet_text])
    conn.commit()
conn.close()
