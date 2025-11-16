"""Tests for the scraper module (async version)."""

import pytest
from linkedin_industry_codes.scraper import scrape_industry_codes


@pytest.mark.asyncio
async def test_scrape_industry_codes():
    """Test that async scraping returns valid data structure."""
    data = await scrape_industry_codes()
    
    # Check top-level structure
    assert "last_updated" in data
    assert "source_url" in data
    assert "total_industries" in data
    assert "industries" in data
    
    # Check industries list
    industries = data["industries"]
    assert isinstance(industries, list)
    assert len(industries) > 0
    
    # Check first industry structure
    first_industry = industries[0]
    required_fields = [
        "industry_id",
        "label",
        "hierarchy",
        "description",
        "category",
        "subcategories",
        "depth",
    ]
    
    for field in required_fields:
        assert field in first_industry, f"Missing field: {field}"
    
    # Validate data types
    assert isinstance(first_industry["industry_id"], int)
    assert isinstance(first_industry["label"], str)
    assert isinstance(first_industry["hierarchy"], str)
    assert isinstance(first_industry["description"], str)
    assert isinstance(first_industry["category"], str)
    assert isinstance(first_industry["subcategories"], list)
    assert isinstance(first_industry["depth"], int)


@pytest.mark.asyncio
async def test_industry_hierarchy_parsing():
    """Test that hierarchy is correctly parsed into category and subcategories."""
    data = await scrape_industry_codes()
    
    for industry in data["industries"][:10]:  # Test first 10
        hierarchy = industry["hierarchy"]
        parts = hierarchy.split(" > ")
        
        assert industry["category"] == parts[0]
        assert industry["subcategories"] == parts[1:]
        assert industry["depth"] == len(parts)


@pytest.mark.asyncio
async def test_scrape_returns_recent_data():
    """Test that scraped data has a recent timestamp."""
    from datetime import datetime, timezone
    
    data = await scrape_industry_codes()
    last_updated = datetime.fromisoformat(data["last_updated"])
    now = datetime.now(timezone.utc)
    
    # Should be within 1 minute
    time_diff = (now - last_updated).total_seconds()
    assert time_diff < 60, "Timestamp should be recent"


@pytest.mark.asyncio
async def test_scrape_includes_metadata():
    """Test that scraped data includes all metadata."""
    data = await scrape_industry_codes()
    
    assert data["source_url"].startswith("https://")
    assert data["total_industries"] > 0
    assert data["total_industries"] == len(data["industries"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

