from helpers.request_handler import RequestHandler
from app.settings import bybit_url

import json
import re

from datetime import datetime

def generate_url(data):
    base_url = "https://www.binance.com/en/support/announcement/"
    slug = data['title'].lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]+", "", slug)  
    code = data['code']
    return f"{base_url}{slug}-{code}"


def extract_symbol_and_launch_time(text: str):
    symbol_pattern = r"(\w+USDT)"
    date_pattern = r"([A-Za-z]+ \d{1,2}, \d{4}, at approximately \d{1,2}(?:AM|PM) UTC)"

    symbol_match = re.search(symbol_pattern, text)
    date_match = re.search(date_pattern, text)

    if not symbol_match or not date_match:
        return None

    symbol = symbol_match.group(1)
    date_str = date_match.group(1)

    launch_time = datetime.strptime(date_str, "%b %d, %Y, at approximately %I%p UTC").timestamp()*1000

    return {"symbol": symbol, "launch_time": int(launch_time)}

def data_dict(soup):
    details = soup.find(id="article-detail-content")
    if details:
        details = details.find('p').text

        return [extract_symbol_and_launch_time(details)]
    else:
        return None
    



def scrape_bybit():
    listings = []
    req_handler = RequestHandler()
    soup = req_handler.get_soup(bybit_url)
    articles = json.loads(soup.find(id="__NEXT_DATA__").text)['props']['pageProps']['articleInitEntity']['list']
    articles = [x for x in articles if ("USDT Perpetual Contracts" in x['title']) and ("Coming Soon" in x['title'])]
    for art in articles:
        url = f"https://announcements.bybit.com/en-US{art['url']}"
        soup2 = req_handler.get_soup(url)
        title = soup2.find('title').text.strip()
        
        listing_data = data_dict(soup2)
        if listing_data:
            listing_data["message"] = title
            listing_data["url"] = url
            listings.extend(listing_data)
        else:
            continue
    return listings