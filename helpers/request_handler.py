import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, TooManyRedirects, HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller


class RequestHandler:
    def __init__(self, retries=3, user_agent=None, use_selenium=False):
        self.retries = retries
        self.use_selenium = use_selenium
        if self.use_selenium:
            chromedriver_autoinstaller.install()
        if user_agent is None:
            self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        else:
            self.user_agent = user_agent

    def _make_request(self, url, method="GET", **kwargs):
        headers = {
            "User-Agent": self.user_agent,
        }
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except (RequestException, Timeout, TooManyRedirects, HTTPError) as e:
            print(f"Request failed: {e}")
            return None

    def _get_selenium_page_source(self, url):
        # Set up a headless Chrome browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--enable-javascript")

        chrome_options.add_argument('--disable-gpu')

        # Suppress logs
        chrome_options.add_argument('--log-level=3')  # Set log level to OFF (3)
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # Initialize the browser with the options
        browser = webdriver.Chrome(options=chrome_options)

        # Navigate to the desired URL
        browser.get(url)

        # Get the page source
        page_source = browser.page_source

        # Close the browser
        browser.quit()

        return page_source

    def get_soup(self, url, parser="html.parser"):
        remaining_retries = self.retries
        while remaining_retries > 0:
            if self.use_selenium:
                page_source = self._get_selenium_page_source(url)
                if page_source:
                    return BeautifulSoup(page_source, parser)
            else:
                response = self._make_request(url)
                if response is not None:
                    return BeautifulSoup(response.content, parser)
            remaining_retries -= 1
            print(f"Retrying... ({self.retries - remaining_retries}/{self.retries})")
        return None

# Example usage:
# handler = RequestHandler(use_selenium=True)
# soup = handler.get_soup("https://example.com")
# print(soup.prettify())
