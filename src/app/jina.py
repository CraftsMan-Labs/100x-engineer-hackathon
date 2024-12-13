import requests


class JinaReader:
    def __init__(self, api_key=None):
        self.base_read_url = "https://r.jina.ai/"
        self.base_search_url = "https://s.jina.ai/"
        self.api_key = api_key

    def read_url(self, url):
        """Read content from a specific URL"""

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        full_url = f"{self.base_read_url}{url}"
        response = requests.get(full_url, headers=headers)
        return response.text

    def search(self, query):
        """Search the web and get results"""

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["X-Retain-Images"] = "none"

        full_url = f"{self.base_search_url}{query}"
        response = requests.get(full_url, headers=headers)
        return response.text
