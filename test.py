import csv
import datetime

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = 'https://www.richardjuzwin.com.au/product/kgv-plate-proof-acsc-70pp7/?sku=29424'
stamp['url'] = url

results_file = 'results.csv'

f = csv.writer(open(results_file, 'w'))
f.writerow(['Name', 'Price', 'Currency','SKU', 'Scrape date', 'Category' , 'Raw text' , 'Image Urls' , 'Link'])

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()

soup = BeautifulSoup(html, "html.parser")

stamp = {} # put the information in a dictionary named 'stamp'
# Every bit of code that could break must be in a try/except block.
try:
	price = soup.find_all("span", {"class":"woocommerce-Price-amount"})[0].get_text()
	price = price.replace(",", "")
	stamp['price'] = price.replace('$','') # Don't want the currency symbol in the text.
except:
	pass # In a loop this would need to be a 'continue' (i.e. skip products with no price)

try:
	name = soup.find_all("h1", {"class":"product_title"})[0].get_text()
	stamp['title'] = name
except:
	stamp['title'] = None

try:
	sku = soup.find_all("span", {"class":"sku"})[0].get_text()
	stamp['sku']=sku
except:
	stamp['sku']=None

try:
	raw_text = soup.find_all("div", {"class":"woocommerce-product-details__short-description"})[0].get_text()
	stamp['raw_text'] = raw_text.replace('¬†','.') # I believe uft-8 isn't the right encoding for this website.
	# I don't want these characters, but instead want the appropriate '.' symbol from the original text.
	# Ideally you would figure out what the correct encoding is, and then change that to utf-8 so that all characters
	# are rendered correctly.
except:
	stamp['raw_text'] = None
	
try:
	category = soup.find_all("span", {"class":"posted_in"})[0].find("a").get_text()
	stamp['category'] = category
except:
	stamp['category'] = None

currency = "AUD"
stamp['currency'] = currency

# image_urls should be a list - as long as your code is in the right format this is fine.
try:
	images = ""
	for img in soup.select('.woocommerce-product-gallery img'):
	    if(images):
	        images = images + ','
	    images = images + img.get('src')
	stamp['image_urls'] = images 
except:
	pass # In a loop this would need to be a 'continue' (i.e. skip products with no images)

# Want the date in format YYYY-MM-DD
scrape_date = datetime.date.today().strftime('%Y-%m-%d')
stamp['scrape_date'] = scrape_date

# print the loop
for key in stamp:
	print(key, stamp[key])

f.writerow([name, price, currency, sku, scrape_date, category, raw_text, images, url])