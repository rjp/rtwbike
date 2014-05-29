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

twitbase = "https://twitter.com/RTWbike/status/%s"

with open(input_html) as file:
    soup = BeautifulSoup(file.read())
    target = soup.find("table", id="distances")
    row = target.find("tr", id="raw-data").extract()
    for i in row("td"): i.clear()
    for d in distances:
        q = copy.deepcopy(row)
        tds = q("td")
        tds[0].string = str(d[0])
        tds[1].string = "%.1f" % (d[1])
        twit_url = twitbase % (d[2])
        twit_a = soup.new_tag("a", href=twit_url)
        twit_a.string = str(d[2])
        tds[2].append(twit_a)
        target.append(q)
    print(soup)
