'''
Python 3.5.2 Script which scrapes hotukdeals.com returning 
the name and temp for results matching the users' input.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd


search = str(input('Please enter product name '))
#search = "xbox"
page = requests.get("http://www.hotukdeals.com/search?action=search&keywords={}".format(search))
soup = BeautifulSoup(page.content, 'html.parser')
container = soup.find_all(class_="space--mt-3")[5]

# Scrape titles of elements and remove extraneous data
titles = []
tlist = [t["href"] for t in container.select("a.thread-title-text")]
for title in tlist:
	titles.append(title.replace("/deals/", "").replace("-", " ").rsplit(" ", 1)[0])


# Scrape temps of elements and convert to int's
str_temps = [t.get_text() for t in container.select(".vwo-vote-container .vwo-temperature")]
temps = list(map(int, str_temps))


# Create a Pandas table and sort on temp
table = pd.DataFrame({
        "titles": titles, 
        "temp": temps, 
    })
temp_sort = table.sort_values("temp", ascending=False)
print(temp_sort)
