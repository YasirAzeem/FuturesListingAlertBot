from helpers.request_handler import RequestHandler
from app.settings import bitget_url
import json



def scrape_bitget(messages):
    listings = []
    req_handler = RequestHandler(use_selenium=True)
    while True:
        try:
            soup = req_handler.get_soup(bitget_url)
            articles = json.loads(soup.find(id="__NEXT_DATA__").text)['props']['pageProps']['sectionArticle']['items']
            break
        except Exception as e:
            print(e)
            continue
    articles = [x for x in articles if ("is now available on futures" in x['title'].lower()) and (x['title'] not in messages)]
    for art in articles:
        listing_data = {}
        listing_data['message'] = art['title'].strip()
        
        listing_data['symbol'] = listing_data['message'].split()[0]
        listing_data['launch_time'] = int(art['showTime'])
        url = f"https://www.bitget.com/en/support/articles/{art['contentId']}"
        listing_data['url'] = url
        listings.append(listing_data)
        
    return listings