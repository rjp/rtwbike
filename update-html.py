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

c.execute("select count(1), min(distance), max(distance), sum(distance) from distances")
(count_dist, min_dist, max_dist, total_dist) = c.fetchone()

nice_total_dist = "%d" % total_dist

c.execute("select set_date, eddington from eddington order by set_date desc limit 1")
(e_date, eddington) = c.fetchone()

next_counts = []
for next_e in range(eddington + 1, eddington + 6):
    c.execute("select count(1), 42 from distances where distance >= ?", [next_e])
    (howmanydone, junk) = c.fetchone()
    howmany = next_e - howmanydone
    next_counts.append([next_e, howmany])

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
        try:
            for x in template.find_all("span", id="repl.%s" % (i)):
                x.string = template.new_string(str(j))
        except:
            pass

next_eddington = next_counts[0][0]
howmany = next_counts[0][1]

with open("progressbar.html") as file:
    progress_template = file.read()

with open(input_html) as file:
    soup = BeautifulSoup(file.read())
    span_replacer(soup, {"count": count_dist, "min": min_dist, "max": max_dist, "total": nice_total_dist})
    span_replacer(soup, {"eddington": eddington, "when": e_date, "next": next_eddington, "howmany": howmany})
    target = soup.find("tbody", id="eddingtons")
    try:
        row = target.find("tr", id="eddings").extract()
        for e in next_counts:
            q, a = clone_row_with_dict(row)
            a['row.next_ed'].string = "%d" % (e[0])
            a['row.howmany'].string = "%d" % (e[1])
            target.append(q)
    except:
        pass
    target = soup.find("tbody", id="distances")
    try:
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
    except:
        pass
    with open(output_html, "w", encoding="utf-8") as output:
        print(soup, file=output)

