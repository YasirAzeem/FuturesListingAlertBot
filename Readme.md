# Crypto Futures Listing Alert App

This app tracks new and upcoming listings about Futures markets on various centralized crypto exchanges like Binance, Bybit, Okx, Kucoin, Mexc, and Bitget. It uses SQLAlchemy to create database models and queries to store listings for each exchange and their launch time. A Telegram bot periodically reminds users of the listing events 2 days, 1 day, 12 hours, 6 hours, 3 hours, 1 hour, 30 minutes, 5 minutes, and when they go live.

## Requirements

- Python 3.9
- aiogram
- bs4
- requests
- SQLAlchemy
- SQLite3

## Project Structure

```
.
├── README.md
├── main.py
├── models.py
├── scraper.py
├── telegram_bot.py
└── utils.py
```

## Description

- `models.py`: Contains the Listing class which is a SQLAlchemy ORM model for the SQLite3 database.
- `scraper.py`: Contains the Scraper class that handles the requests module, creates BeautifulSoup objects for parsing HTML, and extracts relevant data.
- `telegram_bot.py`: Contains the TelegramBot class that handles the Telegram bot functionality and sends alerts to users.
- `utils.py`: Contains utility functions for data processing and conversions.
- `main.py`: The main entry point of the application, which orchestrates the entire workflow.

## Usage

1. Install the required libraries:

```bash
pip install aiogram bs4 requests SQLAlchemy
```

2. Replace the placeholder in `settings.py` with your actual Telegram bot token.

```python
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
```

3. Run the main script:

```bash
python main.py
```

This will start the app, which will scrape the targeted crypto exchanges for new and upcoming listings, store the information in the SQLite3 database, and send reminders through the Telegram bot.