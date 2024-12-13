# Jina AI Web Reader and Search API Usage Guide

## Overview
The `JinaReader` class provides a convenient wrapper for interacting with Jina AI's web reading and search APIs, offering flexible content retrieval and web search capabilities.

## Installation
Ensure you have the `requests` library installed:
```bash
pip install requests
```

## Initialization
Create an instance of `JinaReader` with an optional API key:

```python
from app.jina import JinaReader

# Initialize without an API key
jina_client = JinaReader()

# Initialize with an API key for enhanced features
jina_client_with_key = JinaReader(api_key="your_api_key_here")
```

## Reading Web Content

### Basic URL Reading
Retrieve the content of a web page:

```python
# Read content from a specific URL
url = "https://example.com/article"
content = jina_client.read_url(url)
print(content)
```

### Reading with API Key
Use an API key for potentially improved results:

```python
# Read content with API key authentication
url = "https://complex-webpage.com/detailed-article"
content = jina_client_with_key.read_url(url)
print(content)
```

## Web Search

### Basic Search
Perform a simple web search:

```python
# Perform a web search
query = "Latest AI technology trends"
search_results = jina_client.search(query)
print(search_results)
```

### Search with API Key
Enhance search capabilities with an API key:

```python
# Search with authenticated API key
query = "Machine Learning research papers"
search_results = jina_client_with_key.search(query)
print(search_results)
```

## Error Handling
Always wrap API calls in try-except blocks:

```python
try:
    content = jina_client.read_url("https://example.com")
except requests.RequestException as e:
    print(f"Error reading URL: {e}")

try:
    results = jina_client.search("AI innovations")
except requests.RequestException as e:
    print(f"Search failed: {e}")
```

## Best Practices
- Keep your API key confidential
- Use environment variables for key management
- Implement rate limiting and error handling
- Respect Jina AI's usage terms and conditions

## Notes
- The returned content is raw text/HTML
- For structured data, you may need additional parsing
- API key provides enhanced features and potentially higher rate limits

