# LinkedIn Industry Codes (Async)

A high-performance, async-first Python library and scraper for LinkedIn Industry Codes from Microsoft's official documentation. Built with modern Python async/await patterns for maximum efficiency.

## Features

- ⚡ **Fully Async**: Built with `asyncio` for high-performance parallel operations
- 🔍 **Complete Industry Database**: All LinkedIn industry codes with full metadata
- 🎯 **Smart Matching**: Find similar industries using Levenshtein distance algorithm
- 🔄 **Auto-updated**: Data refreshes daily via GitHub Actions
- 📦 **Easy to Use**: Simple async API with both convenience functions and full-featured matcher
- 🚀 **Fast Batch Processing**: Process multiple queries in parallel efficiently
- 📊 **Rich Data**: Includes industry ID, label, hierarchy, description, and more

## Installation

```bash
pip install linkedin-industry-codes
```

Or with uv (recommended):

```bash
uv pip install linkedin-industry-codes
```

## Quick Start (Async)

### Simple Async Search

```python
import asyncio
from linkedin_industry_codes import get_closest_category

async def main():
    # Find the closest matching industry
    results = await get_closest_category("software development", top_n=3)
    
    for result in results:
        print(f"{result['label']} (Score: {result['similarity_score']:.2%})")
        print(f"  ID: {result['industry_id']}")
        print(f"  Hierarchy: {result['hierarchy']}")

asyncio.run(main())
```

### Batch Processing (Parallel)

```python
import asyncio
from linkedin_industry_codes import get_closest_categories_batch

async def main():
    queries = ["AI", "restaurant", "cybersecurity", "renewable energy"]
    
    # Process all queries in parallel
    results_list = await get_closest_categories_batch(queries, top_n=1)
    
    for query, results in zip(queries, results_list):
        print(f"{query} → {results[0]['label']} ({results[0]['similarity_score']:.2%})")

asyncio.run(main())
```

### Advanced Async Matcher

```python
import asyncio
from linkedin_industry_codes import IndustryMatcher

async def main():
    # Create matcher instance (loads data once)
    matcher = await IndustryMatcher.create()
    
    # Single query
    results = await matcher.find_closest("fintech", top_n=3)
    
    # Batch queries (parallel processing)
    queries = ["tech", "food", "healthcare", "finance", "education"]
    results_list = await matcher.find_closest_batch(queries, top_n=1)
    
    # Browse by category (synchronous)
    categories = matcher.get_all_categories()
    tech_industries = matcher.find_by_category("Technology, Information and Internet")

asyncio.run(main())
```

### Search in Hierarchy

```python
import asyncio
from linkedin_industry_codes import IndustryMatcher

async def main():
    matcher = await IndustryMatcher.create()
    
    # Search within hierarchy paths
    results = await matcher.find_closest(
        "Accommodation Services > Food",
        top_n=5,
        search_field="hierarchy"
    )
    
    for result in results:
        print(f"{result['label']}: {result['hierarchy']}")

asyncio.run(main())
```

## API Reference

### Async Functions

#### `async get_closest_category(query, top_n=1)`

Convenience function for simple async searches.

**Parameters:**
- `query` (str): Search query
- `top_n` (int): Number of results to return

**Returns:** List of dictionaries with industry data and similarity scores

**Example:**
```python
results = await get_closest_category("software")
```

#### `async get_closest_categories_batch(queries, top_n=1)`

Process multiple queries efficiently in parallel.

**Parameters:**
- `queries` (list[str]): List of search queries
- `top_n` (int): Number of results per query

**Returns:** List of result lists, one for each query

**Example:**
```python
results = await get_closest_categories_batch(["tech", "food", "healthcare"])
```

### IndustryMatcher Class

Main class for industry matching with full async support.

#### Initialization

**Async (Recommended):**
```python
matcher = await IndustryMatcher.create()
```

**Sync (Fallback):**
```python
matcher = IndustryMatcher()  # Blocks on data loading
```

#### Methods

**`async find_closest(query, top_n=1, search_field='label')`**
- Find closest matching industries asynchronously
- `search_field`: 'label', 'hierarchy', or 'both'
- Runs CPU-intensive calculations in thread pool

**`async find_closest_batch(queries, top_n=1, search_field='label')`**
- Process multiple queries in parallel
- Much faster than calling `find_closest()` multiple times

**`find_by_category(category)`**
- Get all industries in a specific category (synchronous)

**`get_all_categories()`**
- Get list of all unique categories (synchronous)

## Performance Benefits

The async implementation provides significant performance improvements:

```python
import asyncio
import time
from linkedin_industry_codes import IndustryMatcher

async def benchmark():
    matcher = await IndustryMatcher.create()
    
    queries = ["tech", "food", "healthcare", "finance", "education"] * 10  # 50 queries
    
    start = time.time()
    results = await matcher.find_closest_batch(queries, top_n=1)
    elapsed = time.time() - start
    
    print(f"Processed {len(queries)} queries in {elapsed:.3f}s")
    print(f"Average: {elapsed/len(queries)*1000:.2f}ms per query")

asyncio.run(benchmark())
```

## Data Structure

Each industry record contains:

```python
{
    "industry_id": 2190,
    "label": "Accommodation Services",
    "hierarchy": "Accommodation Services",
    "description": "This industry includes entities that provide...",
    "category": "Accommodation Services",
    "subcategories": [],
    "depth": 1,
    "similarity_score": 0.95,  # Only in search results
    "levenshtein_distance": 2   # Only in search results
}
```

## Running the Scraper

### Manually

```bash
python main.py
```

This will asynchronously:
1. Scrape the latest data from Microsoft's documentation
2. Parse all industry tables
3. Save to `industry_codes.json` with timestamp

### Via GitHub Actions

The included workflow automatically:
- Runs every 24 hours
- Scrapes fresh data asynchronously
- Commits changes if data updated
- Uploads artifacts

## Development

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd industry_codes

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v
```

All tests are async-compatible with `pytest-asyncio`.

### Run Examples

```bash
python examples.py
```

## Why Async?

1. **Parallel Processing**: Process multiple queries simultaneously
2. **Non-blocking I/O**: Efficient network requests for remote data
3. **Scalability**: Handle many concurrent operations
4. **Modern Python**: Follows current best practices
5. **Performance**: Batch operations are significantly faster

## Backward Compatibility

The library supports both async and sync usage:

```python
# Sync fallback (blocks on initialization)
from linkedin_industry_codes import IndustryMatcher
matcher = IndustryMatcher()

# Then use synchronous wrappers or run in event loop
import asyncio
results = asyncio.run(matcher.find_closest("query"))
```

However, we recommend using the async API for best performance.

## CDN Options

The JSON data is served via:

### jsDelivr (Recommended)
```
https://cdn.jsdelivr.net/gh/YOUR_USERNAME/YOUR_REPO@main/industry_codes.json
```

### GitHub Raw
```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/industry_codes.json
```

## Data Source

Data is scraped from Microsoft's official LinkedIn API documentation:
https://learn.microsoft.com/en-us/linkedin/shared/references/reference-tables/industry-codes-v2

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

### v0.1.0 (2025-11-16)
- Initial async-first release
- Web scraper with async httpx
- Levenshtein distance-based matching with async support
- Parallel batch processing
- GitHub Actions automation
- Comprehensive async test suite

## Built With

- `httpx` - Async HTTP client
- `pandas` - Data parsing
- `beautifulsoup4` - HTML parsing
- `python-levenshtein` - Fuzzy matching
- `asyncio` - Async framework

---

**Built with async/await for maximum performance** ⚡
# industry-codes
