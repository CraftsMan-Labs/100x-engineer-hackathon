class ExaAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.exa = None
        self.initialize_client()

    def initialize_client(self):
        """Initialize the Exa client"""
        from exa_py import Exa

        self.exa = Exa(self.api_key)

    def search(self, query, **kwargs):
        """Perform a search with various options"""
        search_params = {
            "use_autoprompt": kwargs.get("use_autoprompt", False),
            "type": kwargs.get("type", "neural"),
            "category": kwargs.get("category", None),
            "num_results": kwargs.get("num_results", 2),
            "include_domains": kwargs.get("include_domains", []),
            "exclude_domains": kwargs.get("exclude_domains", []),
            "start_published_date": kwargs.get("start_date", None),
            "end_published_date": kwargs.get("end_date", None),
        }
        return self.exa.search(query, **search_params)

    def get_contents(self, urls, **kwargs):
        """Retrieve content from specified URLs"""
        content_params = {
            "max_length": kwargs.get("max_length", None),
            "highlights": kwargs.get("highlights", None),
            "summary": kwargs.get("summary", False),
            "subpages": kwargs.get("subpages", None),
            "subpage_target": kwargs.get("subpage_target", None),
        }
        return self.exa.get_contents(urls, **content_params)

    def search_and_contents(self, query, **kwargs):
        """Combined search and content retrieval"""
        search_results = self.search(query, **kwargs)
        urls = [result.url for result in search_results.results]
        return self.get_contents(urls, **kwargs)
