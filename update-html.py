import sys
from bs4 import BeautifulSoup
import copy
import sqlite3

# https://twitter.com/RTWbike/status/464626734521135105

(me, dbfile, input_html) = sys.argv
output_html = input_html + ".new"

conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute("select date, distance, tweet_id  from distances")
distances = c.fetchall()
conn.close()

with open(input_html) as file:
    soup = BeautifulSoup(file.read())
    target = soup.find("table", id="distances")
    row = target.find("tr", id="raw-data").extract()
    for i in ("fish-love-bikes", "cows-go-moo"):
        a = i.split("-")
        q = copy.deepcopy(row)
        tds = q("td")
        tds[0].string = a[0]
        tds[1].string = a[1]
        tds[2].string = a[2]
        target.append(q)
    print(soup)
