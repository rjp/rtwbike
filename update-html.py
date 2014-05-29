import sys
from bs4 import BeautifulSoup
import copy

# https://twitter.com/RTWbike/status/464626734521135105

(me, dbfile, input_html) = sys.argv
output_html = input_html + ".new"

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
