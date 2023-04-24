import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, TooManyRedirects, HTTPError

class RequestHandler:
    def __init__(self, retries=3, user_agent=None):
        self.retries = retries
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

    def get_soup(self, url, parser="html.parser"):
        remaining_retries = self.retries
        while remaining_retries > 0:
            response = self._make_request(url)
            if response is not None:
                return BeautifulSoup(response.content, parser)
            remaining_retries -= 1
            print(f"Retrying... ({self.retries - remaining_retries}/{self.retries})")
        return None

# # Example usage:
# handler = RequestHandler()
# soup = handler.get_soup("https://example.com")
# print(soup.prettify())
