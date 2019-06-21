import csv
import datetime

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = 'https://www.richardjuzwin.com.au/product/kgv-plate-proof-acsc-70pp7/?sku=29424'

results_file = 'results.csv'

f = csv.writer(open(results_file, 'w'))
f.writerow(['Name', 'Price', 'Currency','SKU', 'Scrape date', 'Category' , 'Raw text' , 'Image Urls' , 'Link'])

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()

soup = BeautifulSoup(html, "html.parser")

price = soup.find_all("span", {"class":"woocommerce-Price-amount"})[0].get_text()
price = price.replace(",", "")

name = soup.find_all("h1", {"class":"product_title"})[0].get_text()

sku = soup.find_all("span", {"class":"sku"})[0].get_text()

raw_text = soup.find_all("div", {"class":"woocommerce-product-details__short-description"})[0].get_text()

category = soup.find_all("span", {"class":"posted_in"})[0].find("a").get_text()

currency = "AUD"

images = ""
for img in soup.select('.woocommerce-product-gallery img'):
    if(images):
        images = images + ','
    images = images + img.get('src')

scrape_date = datetime.date.today()

f.writerow([name, price, currency, sku, scrape_date, category, raw_text, images, url])