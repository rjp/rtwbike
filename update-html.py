import sys
from bs4 import BeautifulSoup
import copy
import sqlite3

# https://twitter.com/RTWbike/status/464626734521135105

(me, dbfile, input_html) = sys.argv[:3]

# I do not like green eggs and python's way of defaulting items from a list
output_html = (sys.argv[3:] + [input_html + ".new"])[0]

conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute("select datetime(date), distance, tweet_id from distances order by date desc")
distances = c.fetchall()

c.execute("select count(1), min(distance), max(distance) from distances")
(count_dist, min_dist, max_dist) = c.fetchone()
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

def span_replacer(template, dict):
    for i,j in dict.items():
#        x = template.find("span", id="repl.%s" % (i))
        for x in template.find_all("span", id="repl.%s" % (i)):
            x.string = template.new_string(str(j))

with open("progressbar.html") as file:
    progress_template = file.read()

with open(input_html) as file:
    soup = BeautifulSoup(file.read())
    span_replacer(soup, {"count": count_dist, "min": min_dist, "max": max_dist})
    target = soup.find("tbody", id="distances")
    row = target.find("tr", id="raw-data").extract()
    for d in distances:
        q, a = clone_row_with_dict(row)
        tds = q("td")
        a['row.utc'].string = str(d[0])
        a['row.distance'].string = "%.1f" % (d[1])
        twit_url = twitbase % (d[2])
        twit_a = soup.new_tag("a", href=twit_url)
        twit_a.string = str(d[2])
        progwidth = 100*d[1]/max_dist
        a['row.tweet'].append(twit_a)
        progress = BeautifulSoup(progress_template % (d[1], progwidth, progwidth))
        a["row.progress"].append(progress)
        target.append(q)
    with open(output_html, "w", encoding="utf-8") as output:
        print(soup, file=output)

