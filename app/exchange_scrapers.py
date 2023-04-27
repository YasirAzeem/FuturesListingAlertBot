from exchange_scrapers.binance_futures import scrape_binance
from exchange_scrapers.bybit_futures import scrape_bybit
from exchange_scrapers.bitget_futures import scrape_bitget
from exchange_scrapers.mexc_futures import scrape_mexc
from exchange_scrapers.okx_futures import scrape_okx
from app.db_helpers import add_listing, get_messages_by_exchange
from helpers.logger_config import logger
from asyncio import sleep



async def binance():
    messages = get_messages_by_exchange("Binance Futures")
    listings = scrape_binance(messages)
    for listing in listings:
        add_listing(exchange="Binance Futures",symbol=listing['symbol'], launch_time=listing['launch_time'],message=listing['message'],url=listing["url"])
    return

async def bybit():
    messages = get_messages_by_exchange("Bybit Futures")
    listings = scrape_bybit(messages)
    for listing in listings:
        add_listing(exchange="Bybit Futures",symbol=listing['symbol'], launch_time=listing['launch_time'],message=listing['message'],url=listing["url"])
    return
    
async def bitget():
    messages = get_messages_by_exchange("Bitget Futures")
    listings = scrape_bitget(messages)
    for listing in listings:
        add_listing(exchange="Bitget Futures",symbol=listing['symbol'], launch_time=listing['launch_time'],message=listing['message'],url=listing["url"])
    return


async def mexc():
    messages = get_messages_by_exchange("MEXC Futures")
    listings = scrape_mexc(messages)
    for listing in listings:
        add_listing(exchange="MEXC Futures",symbol=listing['symbol'], launch_time=listing['launch_time'],message=listing['message'],url=listing["url"])
    return

async def okx():
    messages = get_messages_by_exchange("OKX Futures")
    listings = scrape_okx(messages)
    for listing in listings:
        add_listing(exchange="OKX Futures",symbol=listing['symbol'], launch_time=listing['launch_time'],message=listing['message'],url=listing["url"])
    return

async def run_all():
    while True:
        try:
            await binance()
        except Exception as e:
            print(f"Error in Binance Scraping: {e}")
        try:
            await bybit()
        except Exception as e:
            print(f"Error in Bybit Scraping: {e}")
        
        try:
            await bitget()
        except Exception as e:
            print(f"Error in Bitget Scraping: {e}")
        try:
            await mexc()
        except Exception as e:
            print(f"Error in MEXC Scraping: {e}")

        try:
            await okx()
        except Exception as e:
            print(f"Error in OKX Scraping: {e}")
        logger.info("Fresh scrapes done and updated DB.")
        await sleep(15*60)