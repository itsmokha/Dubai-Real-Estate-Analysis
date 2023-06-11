import requests
from requests import get
from bs4 import BeautifulSoup  as soup
import pandas 
import numpy
import re
import json

headers = {"Accept-Language":"en-US, en;q=0.5"}
#url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
url = "https://www.bayut.com/property/details-7377389.html  "
results = requests.get(url,headers=headers)
# print (results)
results_soup = soup(results.text, 'lxml')
print(results_soup)
priceinfo = results_soup.select("[type='application/ld+json']")[1]
propinfo = results_soup.select("[type='application/ld+json']")[2]
# print(data)
priceJson = json.loads(priceinfo.text)['mainEntity']#['offers']['priceSpecification']
price = priceJson['offers'][0]['priceSpecification']['price']
# print ("Price of property: " + str(price))                       # gets price in AED
# sqft = int(json.loads(propinfo.text)["floorSize"]['value'])
sqft = json.loads(propinfo.text)["floorSize"]['value']
sqft = int(sqft.replace(",", ""))
# print ("Property area: " + sqft)
rooms = int(json.loads(propinfo.text)["numberOfRooms"]['value'])
# print("Rooms: " + rooms)
bathrooms = json.loads(propinfo.text)['numberOfBathroomsTotal']
# print("Bathrooms: " + bathrooms)
location = json.loads(propinfo.text)['address']['addressLocality']
# print ("Location: " + location)
pricePerSqft = int(price)/int(sqft)
# print("Price per sqft:" + str(round(pricePerSqft, 2)))
end = []
end.append([price,sqft,rooms,bathrooms,location,pricePerSqft])
df = pandas.DataFrame(end)
# print(df)
# end = []
# end.append([oJson['@type'],oJson['price']])
# for products in oJson:
#     print(products)
        # end.append(products["price"],product["unitText"], product["priceCurrency"], product["@type"])

# df = pandas.DataFrame(end)
# print(df)
# //I want to get this information.. 