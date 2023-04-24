from exchange_scrapers.binance_futures import scrape_binance
from db_helpers import add_listing

def binance():
    listings = scrape_binance()
    for listing in listings:
        add_listing(exchange="Binance Futures",symbol=listing['symbol'], launch_time=listing['timestamp'])
    return

def scrape_bybit():
    # Scrape Bybit listings and store them in the database
    pass

# Implement similar functions for other exchanges
