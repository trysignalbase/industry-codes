# Industry Codes

<div align="center">

![SignalBase Logo](./public/logo.png)

**A programmatic way to access industry classification codes**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Auto-Update](https://img.shields.io/badge/auto--update-daily-green.svg)](https://github.com/trysignalbase/industry-codes/actions)

[CDN URL](#cdn-access) • [Code Examples](#code-examples) • [Python Library](#python-library) • [Data Structure](#data-structure)

</div>

---

## 🎯 Why This Exists

Microsoft maintains a comprehensive table of [Industry Codes](https://learn.microsoft.com/en-us/linkedin/shared/references/reference-tables/industry-codes-v2) on their documentation site. However, accessing this data programmatically is challenging:

- ❌ No official API endpoint
- ❌ Data embedded in HTML tables
- ❌ Requires web scraping and parsing
- ❌ No structured JSON format

**This project solves that.** We automatically scrape, parse, and serve the industry codes as clean JSON via a fast CDN, updated daily.

---

## 🚀 Quick Start

### CDN Access

The easiest way to access the data is via our CDN:

```
https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json
```

The JSON file includes:
- **434 industry codes** organized hierarchically
- **20 main categories** (Finance, Tech, Healthcare, etc.)
- Industry IDs, labels, and descriptions
- Last updated timestamp
- Source URL reference

---

## 💻 Code Examples

### JavaScript / TypeScript

```javascript
// Fetch industry codes
async function getIndustryCodes() {
  const response = await fetch(
    'https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json'
  );
  const data = await response.json();
  
  console.log(`Total industries: ${data.industries.length}`);
  console.log(`Last updated: ${data.metadata.last_updated}`);
  
  // Find all tech industries
  const techIndustries = data.industries.filter(
    industry => industry.category === 'Technology, Information and Internet'
  );
  
  return techIndustries;
}

// Usage
getIndustryCodes().then(industries => {
  industries.forEach(industry => {
    console.log(`${industry.label} (ID: ${industry.id})`);
  });
});
```

### Python

```python
import httpx

# Fetch industry codes
def get_industry_codes():
    response = httpx.get(
        'https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json'
    )
    response.raise_for_status()
    data = response.json()
    
    print(f"Total industries: {len(data['industries'])}")
    print(f"Last updated: {data['metadata']['last_updated']}")
    
    # Find all financial services
    financial = [
        industry for industry in data['industries']
        if industry['category'] == 'Financial Services'
    ]
    
    return financial

# Usage
industries = get_industry_codes()
for industry in industries:
    print(f"{industry['label']} (ID: {industry['id']})")
```

### PHP

```php
<?php

// Fetch industry codes
function getIndustryCodes() {
    $url = 'https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json';
    $json = file_get_contents($url);
    $data = json_decode($json, true);
    
    echo "Total industries: " . count($data['industries']) . "\n";
    echo "Last updated: " . $data['metadata']['last_updated'] . "\n";
    
    // Find all healthcare industries
    $healthcare = array_filter($data['industries'], function($industry) {
        return $industry['category'] === 'Hospitals and Health Care';
    });
    
    return $healthcare;
}

// Usage
$industries = getIndustryCodes();
foreach ($industries as $industry) {
    echo $industry['label'] . " (ID: " . $industry['id'] . ")\n";
}

?>
```

### Go

```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type IndustryData struct {
    Industries []Industry `json:"industries"`
    Metadata   Metadata   `json:"metadata"`
}

type Industry struct {
    ID          int      `json:"id"`
    Label       string   `json:"label"`
    Hierarchy   []string `json:"hierarchy"`
    Description string   `json:"description"`
    Category    string   `json:"category"`
    Depth       int      `json:"depth"`
}

type Metadata struct {
    LastUpdated string `json:"last_updated"`
    Source      string `json:"source"`
    TotalCount  int    `json:"total_count"`
}

func getIndustryCodes() (*IndustryData, error) {
    url := "https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json"
    
    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var data IndustryData
    if err := json.Unmarshal(body, &data); err != nil {
        return nil, err
    }
    
    return &data, nil
}

func main() {
    data, err := getIndustryCodes()
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Total industries: %d\n", len(data.Industries))
    fmt.Printf("Last updated: %s\n", data.Metadata.LastUpdated)
    
    // Find all manufacturing industries
    for _, industry := range data.Industries {
        if industry.Category == "Manufacturing" {
            fmt.Printf("%s (ID: %d)\n", industry.Label, industry.ID)
        }
    }
}
```

---

## 📦 Python Library

For Python users, we provide a full-featured library with fuzzy matching capabilities:

### Installation

```bash
pip install git+https://github.com/trysignalbase/industry-codes.git
```

### Usage

```python
import asyncio
from industry_codes import IndustryMatcher, get_closest_category

async def main():
    # Create matcher (automatically downloads from CDN)
    matcher = await IndustryMatcher.create()
    
    # Find closest match with fuzzy search
    result = matcher.find_closest("software development")
    print(f"Best match: {result['label']} (similarity: {result['similarity']:.2%})")
    
    # Or use the convenience function
    result = await get_closest_category("artificial intelligence")
    print(f"Match: {result['label']} - {result['description']}")
    
    # Search by category
    tech_industries = matcher.find_by_category("Technology, Information and Internet")
    print(f"Found {len(tech_industries)} tech industries")
    
    # Get all categories
    categories = matcher.get_all_categories()
    for category in categories:
        print(f"- {category}")

asyncio.run(main())
```

**Features:**
- 🔍 **Fuzzy matching** using Levenshtein distance
- 🚀 **Async-first** design for performance
- 📥 **Auto-downloads** from CDN (no manual data management)
- 🎯 **Category filtering** and search
- 💯 **Type hints** for better IDE support

See [`examples.py`](./examples.py) for more usage patterns.

---

## 📊 Data Structure

Each industry object contains:

```json
{
  "id": 96,
  "label": "Computer Hardware Manufacturing",
  "hierarchy": [
    "Manufacturing",
    "Computer and Electronics Manufacturing",
    "Computer Hardware Manufacturing"
  ],
  "description": "Manufacturing of computers, computer peripheral equipment, and related electronic products",
  "category": "Manufacturing",
  "subcategories": [],
  "depth": 2
}
```

**Fields:**
- `id` - Microsoft official industry code
- `label` - Human-readable industry name
- `hierarchy` - Full hierarchical path from root to leaf
- `description` - Detailed description of the industry
- `category` - Top-level category
- `subcategories` - List of child industries (if any)
- `depth` - Hierarchy level (0 = root category)

**Metadata:**
```json
{
  "metadata": {
    "last_updated": "2025-11-17T03:18:48.844756+00:00",
    "source": "https://learn.microsoft.com/en-us/linkedin/shared/references/reference-tables/industry-codes-v2",
    "total_count": 434,
    "scraper_version": "1.0.0"
  }
}
```

---

## 🔄 Auto-Updates

The data is automatically updated **every 24 hours** via GitHub Actions. The workflow:

1. ✅ Scrapes latest industry codes from Microsoft's documentation
2. ✅ Parses HTML tables and extracts structured data
3. ✅ Validates and formats as JSON
4. ✅ Commits changes to repository (if any)
5. ✅ Serves via jsDelivr CDN instantly

You always get the freshest data without lifting a finger.

---

## 🏢 Credits

### Developed by [SignalBase](https://trysignalbase.com)

This project is maintained by the team at **SignalBase** - helping businesses build better data infrastructure.

### Data Source

All industry codes are sourced from **Microsoft'sAPI Documentation**:
- [Industry Codes v2 Reference Table](https://learn.microsoft.com/en-us/linkedin/shared/references/reference-tables/industry-codes-v2)

We are grateful to Microsoft for maintaining and documenting these industry classifications. This project simply makes the data more accessible for developers.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The industry codes themselves are maintained by Microsoft/and subject to their terms of service.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report issues** - Found outdated data or bugs? [Open an issue](https://github.com/trysignalbase/industry-codes/issues)
2. **Improve code** - Submit PRs for bug fixes or enhancements
3. **Add examples** - Share how you're using this in your projects
4. **Star the repo** ⭐ - Helps others discover this resource

### Development Setup

```bash
# Clone the repository
git clone https://github.com/trysignalbase/industry-codes.git
cd industry-codes

# Install dependencies with uv
pip install uv
uv sync --extra dev

# Run tests
uv run pytest

# Run linter
uv run ruff check .

# Manually scrape data
uv run python main.py
```

---

## 📚 Resources

- [API Documentation](https://learn.microsoft.com/en-us/linkedin/)
- [How to access the data](./DATA_ACCESS.md)
- [Example implementations](./examples.py)
- [SignalBase Homepage](https://trysignalbase.com)

---

<div align="center">

**Made with ❤️ by [SignalBase](https://trysignalbase.com)**

If this project helps you, consider [⭐ starring it on GitHub](https://github.com/trysignalbase/industry-codes)!

</div>
