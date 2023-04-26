from helpers.request_handler import RequestHandler
from app.settings import okx_url

import pytz
from datetime import datetime

def scrape_okx(messages):
    listings = []
    req_handler = RequestHandler(use_selenium=False)
    soup = req_handler.get_soup(okx_url)
    articles = soup.find_all('li',{'class':'article-list-item'})
    articles = [x for x in articles if ("OKX to" in x.text and "List Perpetual" in x.text and x.text.strip() not in messages)]
    rows = []
    for art in articles:
        coin = art.text.split()[-1] + "USDT"
        url = "https://www.okx.com/support"+art.find('a').get('href')
        rows.append({"symbol":coin, "url":url, "message": art.text.strip()})
    for row in rows:
        soup = req_handler.get_soup(row['url'])
        p = soup.find('div',{'class':'article-body'}).find_all('p')
        p = [x for x in p if "pleased to announce" in str(x)][0].find_all('strong')[-1]
        year = int(soup.find('time').get('title').split('-')[0])
        dt_str = (p.text + " " + str(year))
        dt_str = dt_str.replace('.', '')
        dt = datetime.strptime(dt_str, "%I:%M %p %Z on %B %d %Y")
        
        # Convert to UTC timestamp
        utc_tz = pytz.timezone("UTC")
        dt = utc_tz.localize(dt)
        timestamp = int(dt.timestamp())*1000
        listing_data = row
        # listing_data['message'] = soup.find('h1').text.strip()
        listing_data['launch_time'] = timestamp
        listings.append(listing_data)
    return listings