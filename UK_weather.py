'''
This script scrapes the current temperature from
the metoffice website and displays it to the user.
'''
import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.metoffice.gov.uk/public/weather/forecast/gfnt07u1s")
soup = BeautifulSoup(page.content, 'html.parser')

today = soup.find(class_="weatherTemp")
now = today.select("td i")[0]
temp = now['data-value']
print(temp)