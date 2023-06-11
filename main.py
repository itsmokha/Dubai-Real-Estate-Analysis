from scraper import scrape

frame =pandas.DataFrame(scrape("https://www.bayut.com/to-rent/property/dubai/property/details-7517581.html"))
print(frame)