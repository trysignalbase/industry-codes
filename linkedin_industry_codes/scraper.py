"""Scraper for LinkedIn Industry Codes from Microsoft documentation."""

import asyncio
import json
from datetime import datetime, timezone
from typing import Any

import httpx
import pandas as pd
from bs4 import BeautifulSoup


async def scrape_industry_codes() -> dict[str, Any]:
    """
    Scrape LinkedIn industry codes from Microsoft documentation.
    
    Returns:
        Dictionary containing industry codes data with metadata.
    """
    url = "https://learn.microsoft.com/en-us/linkedin/shared/references/reference-tables/industry-codes-v2"
    
    # Fetch the page asynchronously
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        html_content = response.text
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, "lxml")
    
    # Find all tables in the page
    tables = pd.read_html(html_content)
    
    # Process all tables and combine the data
    all_industries = []
    
    for table in tables:
        # Check if this is an industry table (has the expected columns)
        if "Industry ID" in table.columns and "Label" in table.columns:
            # Convert to records
            records = table.to_dict("records")
            
            for record in records:
                # Clean and structure the data
                industry = {
                    "industry_id": int(record["Industry ID"]),
                    "label": str(record["Label"]).strip(),
                    "hierarchy": str(record["Hierarchy"]).strip(),
                    "description": str(record["Description"]).strip(),
                }
                
                # Parse hierarchy to determine category and subcategories
                hierarchy_parts = industry["hierarchy"].split(" > ")
                industry["category"] = hierarchy_parts[0] if hierarchy_parts else ""
                industry["subcategories"] = hierarchy_parts[1:] if len(hierarchy_parts) > 1 else []
                industry["depth"] = len(hierarchy_parts)
                
                all_industries.append(industry)
    
    # Sort by industry_id for consistency
    all_industries.sort(key=lambda x: x["industry_id"])
    
    # Create the final output structure
    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "source_url": url,
        "total_industries": len(all_industries),
        "industries": all_industries,
    }
    
    return output


async def save_to_json(data: dict[str, Any], filepath: str = "industry_codes.json") -> None:
    """
    Save industry codes data to a JSON file asynchronously.
    
    Args:
        data: Dictionary containing industry codes data.
        filepath: Path to save the JSON file.
    """
    # Use asyncio to write file asynchronously
    await asyncio.to_thread(
        lambda: json.dump(data, open(filepath, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    )


async def main_async():
    """Async main function for scraping."""
    print("Scraping LinkedIn industry codes...")
    data = await scrape_industry_codes()
    print(f"Found {data['total_industries']} industries")
    
    await save_to_json(data)
    print(f"Saved to industry_codes.json")


if __name__ == "__main__":
    asyncio.run(main_async())

