'''
Python 3.5.2 Script which scrapes hotukdeals.com returning 
the name and temp for results matching the users' input.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

search = str(input('Please enter product name '))
page = requests.get("http://www.hotukdeals.com/search?action=search&keywords={}".format(search))
soup = BeautifulSoup(page.content, 'html.parser')
container = soup.find_all(class_="space--mt-3")[5]

titles = []
retailers = []
prices = []
temps = []
paths = []
links = []
URL = "http://www.hotukdeals.com"


# Pull titles, clean and append to titles list
title_list = [t.get_text() for t in container.select("a.thread-title-text")]
[titles.append(t.split("£")[0].strip(' -')) for t in title_list]

# Pull price, retailer, clean and append to price and retailer lists
data = [p.get_text() for p in container.select(".vwo-title-info")]
[retailers.append(r.split("@")[1].split("\n")[0].strip()) for r in data]
[prices.append(p.split("@")[0].strip()) for p in data]

# Pull temps, convert to int's and append to temps list
[temps.append(int(t.get_text())) for t in container.select(".vwo-vote-container .vwo-temperature")]

# Pull paths to details page, append to url then append to links list
[paths.append(p["href"]) for p in container.select("a.thread-title-text")]
[links.append(URL + p) for p in paths]

# Create Pandas table and sort on temp
table = pd.DataFrame({
        "title": titles, 
        "temp": temps, 
        "retailer": retailers, 
        "price": prices,
        "link": links, 
    })
temp_sort = table.sort_values("temp", ascending=False)
print(temp_sort)
