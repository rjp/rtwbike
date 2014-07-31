#! /usr/bin/env python

import sqlite3
import sys
import os
import json
import re
import codecs

def eddington(distances):
    en = 0
    for index, distance in enumerate(sorted(distances, reverse=True)):
        if distance >= index + 1: en = en + 1
    return en

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

extras = None
dbfile = sys.argv[1]
if len(sys.argv) > 2: extras = sys.argv[2]

conn = sqlite3.connect(dbfile)
c = conn.cursor()

# Truncate the Eddington table
c.execute("delete from eddington")

c.execute("select distance, date from distances order by date")
edc = c.fetchall()

print("%s distances, last on %s" % (len(edc), edc[-1][1]))

last_eddington = 0
for qq in range(0, len(edc)):
    xx = edc[0:qq+1]
    yy = [i[0] for i in xx]
    dd = xx[-1][1]
    zz = eddington(yy)
    # print(zz, yy)
    if zz != last_eddington:
        c.execute("insert into eddington values (?,?,?,NULL)", [dd, zz, qq+1])
    last_eddington = zz
conn.commit()
