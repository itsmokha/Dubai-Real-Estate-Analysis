from scraper import scrape
import requests
from requests import get
from bs4 import BeautifulSoup  as soup
import pandas 
import numpy
import re
import json
from tqdm import tqdm
import sys
from datetime import datetime


NUM_PROPERTIES_PER_PAGE = 24

def url_generator(page=1):
    if page == 1:
        url = f'https://www.bayut.com/for-sale/property/dubai/'
    else:
        url = f'https://www.bayut.com/for-sale/property/dubai/page-{page}/'
    return url



# frame =pandas.DataFrame(xscrape("https://www.bayut.com/to-rent/property/dubai/property/details-7517581.html"))
# print(frame)

url = "https://www.bayut.com/to-rent/property/dubai/"
headers = {"Accept-Language":"en-US, en;q=0.5"}
results = requests.get(url,headers=headers)
results_soup = soup(results.text, 'lxml')
# print (results_soup)
num_properties = int(results_soup.find('span',class_='ca3976f7').text.split(' ')[-2].replace(',',''))
print (num_properties)
l = []
# print(results_soup.select("[type='application/ld+json']")[1].text['floorSize'])
pages = (num_properties//NUM_PROPERTIES_PER_PAGE) + 1
# print (num_properties)
# print(pages)

for pageNumber in tqdm(range(1,pages)): 
    # url = url_generator(page=pageNumber)
    # headers = {"Accept-Language":"en-US, en;q=0.5"}
    # results = requests.get(url,headers=headers)
    # results_soup = soup(results.text, 'lxml')
    # info = results_soup.select("[type='application/ld+json']")[1]
    # jon = json.loads(info.text)['itemListElement']
    # # print (l)
    try:
        url = url_generator(page=pageNumber)
        headers = {"Accept-Language":"en-US, en;q=0.5"}
        results = requests.get(url,headers=headers)
        results_soup = soup(results.text, 'lxml')
        info = results_soup.select("[type='application/ld+json']")[1]
        jon = json.loads(info.text)['itemListElement']
        for i in range (1,24):
            try:
                productType = jon[i]['mainEntity']['@type'][1]
                sqft = int(jon[i]['mainEntity']['floorSize']['value'].replace(",", ""))
                price = jon[i]['mainEntity']['offers'][0]['priceSpecification']['price']
                rooms = int(jon[i]['mainEntity']["numberOfRooms"]['value'])
                rooms = int(jon[i]['mainEntity']["numberOfRooms"]['value'])
                bathrooms = jon[i]['mainEntity']['numberOfBathroomsTotal']
                location = jon[i]['mainEntity']['address']['addressLocality']
                lat = jon[i]['mainEntity']['geo']['latitude']
                lon = jon[i]['mainEntity']['geo']['longitude']
                pricePerSqft = int(price)/int(sqft)
                l.append([productType,price,sqft,rooms,bathrooms,location,pricePerSqft,lat,lon])
                print(i, pageNumber)
            except:
                try:
                    l.append(scrape(jon[i]['url']))
                    print('try')
                    print(i, pageNumber)
                except:
                    print("continue")
                    continue
    except:
        break       # If it faces an issue, it means there are no more ads left.

df = pandas.DataFrame(l, columns=['productType','price','sqft','rooms','bathrooms','location','pricePerSqft','latitude','longitude'])
print(df)
df.to_csv('datasets/rent3.csv', index=False)

