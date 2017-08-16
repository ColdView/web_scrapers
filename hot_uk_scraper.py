'''
Python 3.5.2 Script which scrapes hotukdeals.com returning 
the name, retailer, price, link and temp for results matching 
the passed argument.
'''
import argparse
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("query", help="Add a search term " 
                    +"as an argument!", type=str)
args = parser.parse_args()

parameters = {"q": args.query}
page = requests.get("http://www.hotukdeals.com/search?", params=parameters)
soup = BeautifulSoup(page.content, "html.parser")
source = soup.find(class_="thread-list--type-list")

titles = []
retailers = []
prices = []
temps = []

# Extract titles, links and append as hyperlinks to titles list
for t in source.select("a.cept-tt"):
    titles.append('<a href="{u}" target="_blank">{name}</a>' \
                 .format(u=t["href"], name=t.get_text().split("£")[0].strip()))

# Extract retailer info and append to retailers list
[retailers.append(r.get_text()) for r in source.select(".thread-group")]

# Extract price data, clean and append to prices list
for p in source.select(".thread-listImgCell"):
    if "£" in p.get_text():
        x = p.get_text().replace(",", "")
        y = re.search(r"([0-9.]+)", x).group(0)
        prices.append(float(y))
    else:
        prices.append(0.00)

# Extract temps, remove trailing degree symbol and append to temps list
for t in source.select(".vote-temp"):
    t = t.get_text().rstrip("°")
    try:    
        temps.append(int(t))
    except:
        temps.append(0)

# Create Pandas table and sort on temp
df = pd.DataFrame({
        "title": titles,
        "temp": temps,
        "price": prices,
        "retailer": retailers,
    })

table = df[["title", "temp", "price", "retailer"]]
pd.set_option('display.max_colwidth', 250)
pd.set_option('colheader_justify', 'left')
table.sort_values("temp", inplace=True, ascending=False)
table.to_html('deals_table.html', escape=False)
