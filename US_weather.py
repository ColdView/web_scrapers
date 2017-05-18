'''
This script accepts latitudinal and longitudinal
coordinates for a location within the U.S. and returns
the current temperature at that location.
'''

import requests
from bs4 import BeautifulSoup

#Take user input and insert it into the url
lat = input("Please type in the latitude ")
lon = input("Please type in the longitude ")
url = "http://forecast.weather.gov/MapClick.php?lat=%s%slon=%s%s" % (lat, "&", '-', lon)
#Send request for url and parse with bs4
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
temp = soup.find(class_="myforecast-current-lrg").get_text()
print(temp)
