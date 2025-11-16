#!/usr/bin/env python3
"""Main script for scraping LinkedIn industry codes."""

import asyncio

from linkedin_industry_codes.scraper import save_to_json, scrape_industry_codes


async def main():
    """Main entry point for scraping industry codes."""
    print("🔍 Scraping LinkedIn Industry Codes...")
    print("=" * 60)
    
    try:
        # Scrape the data asynchronously
        data = await scrape_industry_codes()
        
        print(f"✅ Successfully scraped {data['total_industries']} industries")
        print(f"📅 Last updated: {data['last_updated']}")
        print(f"🔗 Source: {data['source_url']}")
        
        # Show some statistics
        categories = set(industry["category"] for industry in data["industries"])
        print(f"📊 Found {len(categories)} main categories:")
        for category in sorted(categories)[:10]:  # Show first 10
            count = sum(1 for ind in data["industries"] if ind["category"] == category)
            print(f"   • {category}: {count} industries")
        
        if len(categories) > 10:
            print(f"   ... and {len(categories) - 10} more categories")
        
        # Save to JSON asynchronously
        output_file = "industry_codes.json"
        await save_to_json(data, output_file)
        print(f"\n💾 Saved to {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
