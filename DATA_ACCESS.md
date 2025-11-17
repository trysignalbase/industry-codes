# LinkedIn Industry Codes - Data Access

Your scraped industry codes JSON is automatically available via REST GET requests!

## 🌐 Public REST Endpoints

### GitHub Raw (Direct)
```
https://raw.githubusercontent.com/trysignalbase/industry-codes/main/industry_codes.json
```

**Usage:**
```bash
curl https://raw.githubusercontent.com/trysignalbase/industry-codes/main/industry_codes.json
```

### jsDelivr CDN (Recommended - Fast & Cached)
```
https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json
```

**Usage:**
```bash
curl https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json
```

**Benefits:**
- ⚡ Global CDN distribution
- 🚀 Fast response times
- 💾 Automatic caching
- 🆓 Free forever
- 📌 Version pinning support

### Version-Specific URLs (jsDelivr)

**Latest from main:**
```
https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json
```

**Specific commit:**
```
https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@COMMIT_HASH/industry_codes.json
```

**Specific tag/version:**
```
https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@v1.0.0/industry_codes.json
```

## 📊 Data Format

The JSON contains:
```json
{
  "last_updated": "2025-11-17T12:00:00+00:00",
  "source_url": "https://learn.microsoft.com/...",
  "total_industries": 150,
  "industries": [
    {
      "industry_id": 2190,
      "label": "Accommodation Services",
      "hierarchy": "Accommodation Services",
      "description": "This industry includes...",
      "category": "Accommodation Services",
      "subcategories": [],
      "depth": 1
    }
  ]
}
```

## 🔄 Update Frequency

- Automatically updated every 24 hours via GitHub Actions
- Check `last_updated` field in JSON for timestamp
- Manual updates can be triggered via GitHub Actions UI

## 💻 Usage Examples

### cURL
```bash
# Download the JSON
curl -o industry_codes.json https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json

# Get just the total count
curl -s https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json | jq '.total_industries'

# Get all category names
curl -s https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json | jq '.industries[].category' | sort -u
```

### Python
```python
import httpx

# Sync
response = httpx.get("https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json")
data = response.json()
print(f"Total industries: {data['total_industries']}")

# Async
import asyncio
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json"
        )
        return response.json()

data = asyncio.run(fetch_data())
```

### JavaScript/Node.js
```javascript
// Using fetch
const response = await fetch('https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json');
const data = await response.json();
console.log(`Total industries: ${data.total_industries}`);

// Using axios
const axios = require('axios');
const { data } = await axios.get('https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json');
console.log(`Total industries: ${data.total_industries}`);
```

### Go
```go
package main

import (
    "encoding/json"
    "net/http"
)

func main() {
    resp, _ := http.Get("https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json")
    defer resp.Body.Close()
    
    var data map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&data)
    println("Total industries:", data["total_industries"])
}
```

### Rust
```rust
use reqwest;
use serde_json::Value;

#[tokio::main]
async fn main() {
    let data: Value = reqwest::get("https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json")
        .await
        .unwrap()
        .json()
        .await
        .unwrap();
    
    println!("Total industries: {}", data["total_industries"]);
}
```

## 🛠️ Integration with Your App

The library automatically uses this endpoint as a fallback:

```python
from industry_codes import IndustryMatcher

# This will download from GitHub if no local data exists
matcher = await IndustryMatcher.create()

# Now you can search
results = await matcher.find_closest("software development")
```

## 🔒 CORS

Both GitHub Raw and jsDelivr support CORS, so you can use these endpoints from browsers:

```javascript
fetch('https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 📈 Rate Limits

- **GitHub Raw**: No official limit, but recommended to cache
- **jsDelivr CDN**: No rate limits, globally distributed

## 🎯 Best Practices

1. **Use jsDelivr for production** - it's faster and more reliable
2. **Cache the response** - data only updates once per day
3. **Check `last_updated`** - to know when data was refreshed
4. **Handle errors gracefully** - network requests can fail

## 📝 Notes

- Data is stored in the `main` branch of the repository
- The scraper runs daily at midnight UTC
- Manual triggers available via GitHub Actions
- File size: ~50-200KB (depends on number of industries)

---

**Your data is now publicly accessible via REST! 🎉**

