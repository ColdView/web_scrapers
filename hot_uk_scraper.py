'''
Python 3.5.2 Script which scrapes hotukdeals.com returning 
the name and temp for results matching the users' input.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

query = "ps4"#str(input("Please enter product name "))
parameters = {"q": query}
page = requests.get("http://www.hotukdeals.com/search?", params=parameters)
soup = BeautifulSoup(page.content, "html.parser")
source = soup.find(class_="thread-list--type-list")

titles = []
retailers = []
price_data= []
prices = []
temps = []
links = []
URL = "http://www.hotukdeals.com"

# Pull titles, clean and append to titles list
[titles.append(t.get_text().split("£")[0].strip()) for t in source.select("a.cept-tt")]
# Pull retailer and append to retailer list
[retailers.append(r.get_text()) for r in source.select(".thread-group")]

[price_data.append(i.get_text()) for i in source.select(".thread-listImgCell")]

for p in price_data:
	if "£" in p:
		x = p.strip("GetGet deal £")
		prices.append(float(x))
	else:
		prices.append(0.00)
# Pull temps, convert to int's remove trailing degree symbol and append to temps list

for t in source.select(".vote-temp"):
	t = t.get_text().rstrip("°")
	try:	
		temps.append(int(t))
	except:
		temps.append(0)

[links.append(p["href"]) for p in source.select("a.cept-tt.thread-link")]

# Create Pandas table and sort on temp

df = pd.DataFrame({
        "title": titles,
        "temp": temps,
        "price": prices,
        "retailer": retailers,
        "link": links
    })
table = df[["title", "temp", "price", "retailer", "link"]]
pd.set_option('display.max_colwidth', 250)
pd.set_option('max_rows', 100)
pd.set_option('colheader_justify', 'left')
table.sort_values("temp", inplace=True, ascending=False)
table.to_html('deals_table.html', escape=False)
