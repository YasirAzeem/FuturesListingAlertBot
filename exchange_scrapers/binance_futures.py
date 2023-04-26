from helpers.request_handler import RequestHandler
from app.settings import binance_url

import json
import re
import time
from datetime import datetime

def generate_url(data):
    base_url = "https://www.binance.com/en/support/announcement/"
    slug = data['title'].lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]+", "", slug)  
    code = data['code']
    return f"{base_url}{slug}-{code}"


def table_dict(table, title, url):
    # Extract header names
    header_cells = table.find_all('tr')[0].find_all('td')
    header_names = [cell.get_text(strip=True) for cell in header_cells]

    # Extract data rows
    data_rows = table.find_all('tr')[1:]

    # Create a dictionary from the data rows
    data = {}
    for header_name in header_names:
        data[header_name] = []

    for row in data_rows:
        cells = row.find_all('td')
        for i, cell in enumerate(cells):
            data[header_names[i]].append(cell.get_text(strip=True))
    output_data = []
    for ky in list(data.keys())[1:]:
        sym_dict = {}
        sym_dict['symbol'] = ky
        launch_time_dt = datetime.strptime(data[ky][0].strip(), "%Y-%m-%d %H:%M (UTC)")
        sym_dict['launch_time'] =   1000*int(time.mktime(launch_time_dt.timetuple()))
        sym_dict["message"] = title
        sym_dict["url"] = url      
        output_data.append(sym_dict)
        
    return output_data



def scrape_binance(messages):
    listings = []
    req_handler = RequestHandler()
    soup = req_handler.get_soup(binance_url)
    catalogs = json.loads(soup.find(id="__APP_DATA").text)['routeProps']['ce50']['catalogs']
    articles = []
    for cat in catalogs:
        articles.extend(cat['articles'])
    articles = json.loads(soup.find(id="__APP_DATA").text)['routeProps']['ce50']['catalogs'][0]['articles']
    articles = [x for x in articles if ("Binance Futures Will Launch USDT-Margined" in x['title']) and (x['title'] not in messages)]
    for art in articles:
        url = generate_url(art)
        soup2 = req_handler.get_soup(url)
        title = soup2.find('title').text.strip()
        table = soup2.find('table')
        listing_data = table_dict(table, title, url)
        listings.extend(listing_data)
    return listings