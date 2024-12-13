# Exa API Wrapper Usage Guide

## Overview
The `ExaAPI` class provides a convenient wrapper for interacting with the Exa search API, offering flexible search and content retrieval capabilities.

## Installation
Ensure you have the `exa-py` package installed:
```bash
pip install exa-py
```

## Initialization
Create an instance of `ExaAPI` with your Exa API key:

```python
from app.exa import ExaAPI

# Initialize the Exa API client
exa_client = ExaAPI(api_key="your_api_key_here")
```

## Search Methods

### Basic Search
Perform a simple search with default parameters:

```python
# Basic search
results = exa_client.search("AI technology trends")
for result in results.results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
```

### Advanced Search
Customize your search with additional parameters:

```python
# Advanced search with custom parameters
results = exa_client.search(
    query="Machine Learning",
    use_autoprompt=True,
    num_results=5,
    include_domains=["mit.edu", "stanford.edu"],
    start_date="2023-01-01",
    end_date="2024-01-01"
)
```

### Search and Retrieve Contents
Combine search and content retrieval in one step:

```python
# Search and get contents
results = exa_client.search_and_contents(
    query="Latest AI research",
    num_results=3,
    summary=True
)
for result in results.results:
    print(f"URL: {result.url}")
    print(f"Summary: {result.text}")
```

### Retrieve Contents for Specific URLs
Get detailed content for known URLs:

```python
# Get contents for specific URLs
urls = ["https://example.com/article1", "https://example.com/article2"]
contents = exa_client.get_contents(
    urls, 
    max_length=1000,
    highlights=True,
    summary=True
)
```

## Parameters Reference

### Search Parameters
- `query`: Search query string (required)
- `use_autoprompt`: Enhance query with AI (default: False)
- `type`: Search type (default: "neural")
- `num_results`: Number of results (default: 10)
- `include_domains`: Whitelist domains
- `exclude_domains`: Blacklist domains
- `start_date`: Earliest publication date
- `end_date`: Latest publication date

### Content Retrieval Parameters
- `max_length`: Limit content length
- `highlights`: Extract key highlights
- `summary`: Generate content summary
- `subpages`: Include subpages
- `subpage_target`: Specific subpage targeting

## Error Handling
Always wrap API calls in try-except blocks:

```python
try:
    results = exa_client.search("Your query")
except Exception as e:
    print(f"Search failed: {e}")
```

## Best Practices
- Keep your API key confidential
- Use environment variables for key management
- Implement rate limiting and error handling
- Respect Exa's usage terms and conditions
```
