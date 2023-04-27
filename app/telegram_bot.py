import asyncio
from aiogram import Bot, Dispatcher, types

from datetime import datetime, timedelta

from app.models import Listing, Session
from app.settings import TELEGRAM_TOKEN, CHAT_ID
from app.exchange_scrapers import run_all
from helpers.telegram_message import create_telegram_message
from helpers.logger_config import setup_logger

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
logger = setup_logger()

async def send_reminders():
    reminder_intervals = [
        timedelta(days=2),
        timedelta(days=1),
        timedelta(hours=12),
        timedelta(hours=6),
        timedelta(hours=3),
        timedelta(hours=1),
        timedelta(minutes=30),
        timedelta(minutes=5),
    ]

    while True:
        session = Session()
        now = datetime.utcnow()

        listings = session.query(Listing).all()
        for listing in listings:
            remaining_time = datetime.utcfromtimestamp(listing.launch_time/1000) - now
            if listing.new_listing and remaining_time.total_seconds()>0:
                await bot.send_message(chat_id=CHAT_ID, text=create_telegram_message(listing))
                listing.new_listing = False
                session.commit()
            else:

                for interval in reminder_intervals:
                    interval_timedelta = timedelta(seconds=interval.total_seconds())
                    if timedelta(0) <= remaining_time <= interval_timedelta:
                        # message = f"Reminder: {listing.symbol} will be listed on {listing.exchange} in {remaining_time}. {listing.message}\n{listing.url}"
                        await bot.send_message(chat_id=CHAT_ID, text=create_telegram_message(listing))
                        break  # Avoid sending multiple reminders for the same listing
        logger.info("DB Check performed, No more alerts for now!")
        await asyncio.sleep(60)

async def on_startup(dp):
    asyncio.create_task(run_all())
    asyncio.create_task(send_reminders())
    await bot.send_message(chat_id=CHAT_ID, text="Bot has been started")
    logger.info("Bot has started.")

async def on_shutdown(dp):
    await bot.send_message(chat_id=CHAT_ID, text="Bot has been stopped")
    logger.info("Bot has stopped.")

