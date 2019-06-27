import csv
import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_category_items(category_url):
    items = []
    try:
        category_html = get_html(category_url)
        for item in category_html.select('.woocommerce-loop-product__link'):
            items.append(item.get('href'))
    except: 
        pass

    return items

def get_categories():
    url = 'https://www.richardjuzwin.com.au/stamps/'
    items = []
    try:
        html = get_html(url)
        category_items = html.find_all('li', {'class': 'product-category'})
        for category_item in category_items:
            item = category_item.find('a').get('href')
            items.append(item)
    except: 
        pass
 
    return items

def get_details(url):
    
    stamp = {}

    try:
       html = get_html(url)
    except:
       return stamp

    try:
        price = html.find_all("span", {"class":"woocommerce-Price-amount"})[0].get_text()
        price = price.replace(",", "")
        stamp['price'] = price.replace('$','')
    except:
        stamp['price'] = None

    try:
        name = html.find_all("h1", {"class":"product_title"})[0].get_text()
        stamp['title'] = name
    except:
        stamp['title'] = None

    try:
        sku = html.find_all("span", {"class":"sku"})[0].get_text()
        stamp['sku']=sku
    except:
        stamp['sku']=None

    try:
        raw_text = html.find_all("div", {"class":"woocommerce-product-details__short-description"})[0].get_text()
        stamp['raw_text'] = raw_text.replace('¬†','.') # I believe uft-8 isn't the right encoding for this website.
    except:
        stamp['raw_text'] = None

    try:
        category = html.find_all("span", {"class":"posted_in"})[0].get_text()
        category = category.replace('Categories:','')
        stamp['category'] = category
    except:
        stamp['category'] = None

    currency = "AUD"
    stamp['currency'] = currency

    # image_urls should be a list
    images = ""
    try:
        for img in html.select('.woocommerce-product-gallery img'):
            if(images):
                images = images + ','
            images = images + img.get('src')
    except:
         pass 

    stamp['image_urls'] = images 

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url

    return stamp

# empty csv output file and write header
f = csv.writer(open('results.csv', 'w', encoding="utf8", newline=""))
f.writerow(['Name', 'Price', 'Currency','SKU', 'Scrape date', 'Category' , 'Raw text' , 'Image Urls' , 'Link'])

# initialize stamps array
stamps = []

# loop through all categories
categories = get_categories()
for category in categories:
    # loop trough every item in current category
    category_items = get_category_items(category)
    for category_item in category_items:
        # get current item details 
        stamp = get_details(category_item)
        if stamp:
            stamps.append(stamp)
            # write current item details in output csv 
            f.writerow([stamp['title'], stamp['price'], stamp['currency'], stamp['sku'], stamp['scrape_date'], stamp['category'], stamp['raw_text'], stamp['image_urls'], stamp['url']])
