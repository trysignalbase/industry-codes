"""Tests for linkedin_industry_codes package (async version)."""

import pytest
from linkedin_industry_codes import (
    IndustryMatcher,
    get_closest_categories_batch,
    get_closest_category,
)


@pytest.mark.asyncio
async def test_get_closest_category():
    """Test the async convenience function."""
    results = await get_closest_category("software", top_n=1)
    assert len(results) == 1
    assert "label" in results[0]
    assert "industry_id" in results[0]
    assert "similarity_score" in results[0]


@pytest.mark.asyncio
async def test_get_closest_categories_batch():
    """Test the batch convenience function."""
    queries = ["software", "restaurant", "healthcare"]
    results_list = await get_closest_categories_batch(queries, top_n=1)

    assert len(results_list) == len(queries)
    for results in results_list:
        assert len(results) == 1
        assert "label" in results[0]


@pytest.mark.asyncio
async def test_industry_matcher_async_creation():
    """Test IndustryMatcher async creation."""
    matcher = await IndustryMatcher.create()
    assert matcher.industries is not None


def test_industry_matcher_sync_initialization():
    """Test IndustryMatcher synchronous initialization."""
    matcher = IndustryMatcher()
    assert matcher.industries is not None


@pytest.mark.asyncio
async def test_find_closest():
    """Test async find_closest method."""
    matcher = await IndustryMatcher.create()
    results = await matcher.find_closest("technology", top_n=3)

    assert len(results) <= 3
    assert all("similarity_score" in r for r in results)
    assert results[0]["similarity_score"] >= results[-1]["similarity_score"]


@pytest.mark.asyncio
async def test_find_closest_batch():
    """Test batch finding functionality."""
    matcher = await IndustryMatcher.create()
    queries = ["tech", "food", "finance"]
    results_list = await matcher.find_closest_batch(queries, top_n=2)

    assert len(results_list) == len(queries)
    for results in results_list:
        assert len(results) <= 2


def test_get_all_categories():
    """Test get_all_categories method."""
    matcher = IndustryMatcher()
    categories = matcher.get_all_categories()

    assert isinstance(categories, list)
    assert len(categories) > 0
    assert all(isinstance(c, str) for c in categories)


def test_find_by_category():
    """Test find_by_category method."""
    matcher = IndustryMatcher()
    categories = matcher.get_all_categories()

    if categories:
        results = matcher.find_by_category(categories[0])
        assert isinstance(results, list)


@pytest.mark.asyncio
async def test_similarity_score_range():
    """Test that similarity scores are in valid range."""
    matcher = await IndustryMatcher.create()
    results = await matcher.find_closest("test query", top_n=5)

    for result in results:
        score = result["similarity_score"]
        assert 0 <= score <= 1, f"Similarity score {score} out of range"


@pytest.mark.asyncio
async def test_search_fields():
    """Test different search field options."""
    matcher = await IndustryMatcher.create()

    query = "software"

    # Test each search field
    for field in ["label", "hierarchy", "both"]:
        results = await matcher.find_closest(query, top_n=1, search_field=field)
        assert len(results) == 1
        assert "similarity_score" in results[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
