from helpers.request_handler import RequestHandler
from app.settings import mexc_url
import json
import re
import pytz
from datetime import datetime
from helpers.logger_config import logger


def get_coin_names(rows):
    for entry in rows:
        entry['message'] = entry['title']
        title = entry['title'].split(" USDT-M Perpetual Futures")[0]
        matches = re.findall(r'\b[A-Z0-9]{2,}(?=[ ,]|\b)', title)
        coins = [coin for coin in matches if coin not in ('MEXC', 'USDT', 'M')]
        entry['coins'] = coins
        entry['url'] = f"https://www.mexc.com/support/articles/{entry['id']}"
        
    return rows

def scrape_mexc(messages):
    listings = []
    req_handler = RequestHandler(use_selenium=False)
    soup = req_handler.get_soup(mexc_url)
    data = json.loads(soup.text)
    if data.get('results'):
        rows = [x for x in data['results'] if ("USDT-M Perpetual Futures" in x['title']) and ("MEXC Will List " in x['title']) and (x['title'] not in messages)]
        rows = get_coin_names(rows)
        for row in rows:
            req_handler = RequestHandler(use_selenium=True)
            soup = req_handler.get_soup(row['url'])
            if len(row['coins'])>1:
                
                table = soup.find('table')
                trs = table.find_all('tr')[1:]
                utc_tz = pytz.timezone('UTC')
                data = []

                for tr in trs:
                    cols = tr.find_all('td')
                    if cols[0].has_attr('rowspan'):
                        timestamp_col = cols[0].text
                        dt = datetime.strptime(timestamp_col, "%H:%M, %B %d")
                        dt = dt.replace(year=datetime.now().year)
                        dt = utc_tz.localize(dt)
                        timestamp = int(dt.timestamp()) * 1000

                    pair = cols[-1].text.strip()
                    listing_data = row
                    listing_data['symbol'] = pair+"USDT"
                    listing_data['launch_time'] = timestamp
                    
                    listings.append(listing_data)

            elif len(row['coins'])==1:
                ps = soup.find_all('p')
                cc = ps[1].text

                # Extract the date and time
                datetime_match = re.search(r'(\d{2}:\d{2}), (\w+ \d{1,2}, \d{4})', cc)
                if datetime_match:
                    time_str = datetime_match.group(1)
                    date_str = datetime_match.group(2)
                    dt_str = f"{date_str} {time_str}"
                    dt = datetime.strptime(dt_str, "%B %d, %Y %H:%M")

                    # Convert to UTC timestamp
                    utc_tz = pytz.timezone("UTC")
                    dt = utc_tz.localize(dt)
                    timestamp = int(dt.timestamp()) * 1000
                    listing_data = row
                    listing_data['symbol'] = row['coins'][0]
                    listing_data['launch_time'] = timestamp
                    listings.append(listing_data)
    else:
        logger.error(data)
    return listings