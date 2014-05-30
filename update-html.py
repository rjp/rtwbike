import sys
from bs4 import BeautifulSoup
import copy
import sqlite3

# https://twitter.com/RTWbike/status/464626734521135105

(me, dbfile, input_html) = sys.argv
output_html = input_html + ".new"

conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute("select datetime(date), distance, tweet_id from distances order by date desc")
distances = c.fetchall()
conn.close()

twitbase = "https://twitter.com/RTWbike/status/%s"

def clone_row_with_dict(bsrow):
    q = copy.deepcopy(bsrow)
    tds = q("td")
    a = {}
    for i in tds:
        i.clear()
        a[i['id']] = i
        del(i['id'])
    return q, a

with open(input_html) as file:
    soup = BeautifulSoup(file.read())
    target = soup.find("table", id="distances")
    row = target.find("tr", id="raw-data").extract()
    for d in distances:
        q, a = clone_row_with_dict(row)
        tds = q("td")
        a['row.utc'].string = str(d[0])
        a['row.distance'].string = "%.1f" % (d[1])
        twit_url = twitbase % (d[2])
        twit_a = soup.new_tag("a", href=twit_url)
        twit_a.string = str(d[2])
        a['row.tweet'].append(twit_a)
        target.append(q)
    print(soup)
