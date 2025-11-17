"""Pytest fixtures for industry_codes tests."""

import pytest
from industry_codes.scraper import scrape_industry_codes


@pytest.fixture(scope="module")
async def scraped_data():
    """
    Fixture that scrapes industry codes once and reuses across all tests in the module.

    Using 'module' scope means this will be called once per test file,
    not once per test function.
    """
    print("\n🔍 Scraping industry codes (cached for all tests)...")
    data = await scrape_industry_codes()
    print(f"✅ Scraped {data['total_industries']} industries")
    return data


@pytest.fixture(scope="session")
def event_loop_policy():
    """
    Configure the event loop policy for async tests.
    """
    import asyncio

    return asyncio.get_event_loop_policy()
