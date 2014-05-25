#! /usr/bin/env python

import sqlite3
import sys
import os
import json

dbfile = sys.argv[1]
json_out = sys.argv[2]

conn = sqlite3.connect(dbfile)
c = conn.cursor()

with open(json_out, "w") as file:
    c.execute("select * from distances")
    distances = c.fetchall()
    json.dump(distances, file)
