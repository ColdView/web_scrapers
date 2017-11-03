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
#page = requests.get("https://www.hotukdeals.com/search?q=xbox")
page = requests.get("http://www.hotukdeals.com/search?", params=parameters)
soup = BeautifulSoup(page.content, "html.parser")
articles = soup.find_all("article")
source = soup.find(class_="thread-list--type-list")

titles = []
retailers = []
prices = []
temps = []
i=0
# ----------PRICES----------
for p in articles:
    if p.select(".thread-price"):
        price = p.select(".thread-price")[0].get_text().strip("£")
        prices.append(price)
    else:
        prices.append(0)

# ----------TITLES-----------
for tt in articles:
    t = tt.select("a.thread-link")[0]
    titles.append('<a href="{u}" target="_blank">{name}</a>' \
                 .format(u=t["href"], name=t.get_text().split("£")[0].strip()))


# -------RETAILERS------------
[retailers.append(r.get_text()) for r in source.select(".cept-merchant-name")]


# -----------TEMPS------------
for t in articles:
    if t.select(".vote-temp "):
        temp = t.select(".vote-temp ")[0].get_text()
        y = re.search(r"([0-9.-]+)", temp).group(0)
        temps.append(int(y))
    else:
        temps.append(0)



print(prices)
print(temps)

print("Temps = "+str(len(temps)))
print("Articles = "+str(len(articles)))
print("Prices = "+str(len(prices)))
print("Titles = "+str(len(titles)))
print("Retailers = "+str(len(retailers)))


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




