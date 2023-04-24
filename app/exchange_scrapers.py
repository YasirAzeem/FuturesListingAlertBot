from exchange_scrapers.binance_futures import scrape_binance
from exchange_scrapers.bybit_futures import scrape_bybit
from db_helpers import add_listing

def binance():
    listings = scrape_binance()
    for listing in listings:
        add_listing(exchange="Binance Futures",symbol=listing['symbol'], launch_time=listing['timestamp'])
    return

def scrape_bybit():
    listings = scrape_bybit()
    for listing in listings:
        add_listing(exchange="Bybit Futures",symbol=listing['symbol'], launch_time=listing['timestamp'])
    return
    
def scrape_okx():
    pass